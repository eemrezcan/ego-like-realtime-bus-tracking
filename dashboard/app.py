from __future__ import annotations

from datetime import datetime, timezone

import pydeck as pdk
import streamlit as st

from dashboard.api_client import DashboardApiClient, DashboardApiError
from dashboard.config import load_dashboard_settings
from dashboard.view_models import (
    OCCUPANCY_COLORS,
    build_bus_table_rows,
    build_map_dataframe,
    filter_buses_by_line,
    summarize_delay_label,
)


st.set_page_config(
    page_title="EGO Benzeri Otobus Takip Dashboard",
    page_icon=":bus:",
    layout="wide",
)


def main() -> None:
    settings = load_dashboard_settings()
    _inject_styles()

    st.title("EGO Benzeri Gercek Zamanli Otobus Takip Dashboard")
    st.caption(
        "Sentetik telemetri, MQTT akisi, bulutta isleme ve canli izleme zincirinin canli demo ekrani."
    )

    with st.sidebar:
        st.header("Baglanti")
        base_url = st.text_input("API Base URL", value=settings.api_base_url)
        selected_line_default = settings.default_selected_line or "Tum Hatlar"
        refresh_requested = st.button("Veriyi Yenile", width="stretch")
        st.caption("API ayakta ise kartlar ve harita bu veri kaynagindan beslenir.")
        st.divider()
        st.header("Canli Akis")
        auto_refresh_enabled = st.toggle(
            "Otomatik yenile",
            value=settings.auto_refresh_seconds > 0,
            help="Dashboard acik kaldigi surece veriyi belirli aralikla yeniden ceker.",
        )
        refresh_interval = st.slider(
            "Yenileme araligi (sn)",
            min_value=2,
            max_value=15,
            value=max(settings.auto_refresh_seconds, 5),
            disabled=not auto_refresh_enabled,
        )
        st.caption(
            "Otobus konumlari, simulator yeni veri gonderdikce haritada guncellenir."
        )

    if refresh_requested:
        st.cache_data.clear()

    try:
        initial_lines = _get_lines(base_url)
    except DashboardApiError as exc:
        _render_unavailable_state(base_url, str(exc))
        return

    line_options = ["Tum Hatlar"] + [line["line_id"] for line in initial_lines]
    selected_line = st.sidebar.selectbox(
        "Hat Filtresi",
        options=line_options,
        index=line_options.index(selected_line_default)
        if selected_line_default in line_options
        else 0,
        key="dashboard-line-filter",
    )

    run_every = f"{refresh_interval}s" if auto_refresh_enabled else None

    @st.fragment(run_every=run_every)
    def render_live_dashboard() -> None:
        try:
            health = _get_health(base_url)
            summary = _get_summary(base_url)
            lines = _get_lines(base_url)
            buses = _get_buses(base_url)
        except DashboardApiError as exc:
            _render_unavailable_state(base_url, str(exc))
            return

        filtered_buses = filter_buses_by_line(buses, selected_line)

        _render_status_banner(health, summary, auto_refresh_enabled, refresh_interval)
        _render_stream_freshness(summary)
        _render_summary_cards(summary)
        _render_main_grid(lines, filtered_buses)

    render_live_dashboard()


@st.cache_data(ttl=2)
def _get_health(base_url: str) -> dict[str, object]:
    return DashboardApiClient(base_url=base_url).get_health()


@st.cache_data(ttl=2)
def _get_summary(base_url: str) -> dict[str, object]:
    return DashboardApiClient(base_url=base_url).get_summary()


@st.cache_data(ttl=2)
def _get_lines(base_url: str) -> list[dict[str, object]]:
    return DashboardApiClient(base_url=base_url).get_lines()


@st.cache_data(ttl=2)
def _get_buses(base_url: str) -> list[dict[str, object]]:
    return DashboardApiClient(base_url=base_url).get_buses()


def _render_unavailable_state(base_url: str, error_message: str) -> None:
    st.error("Dashboard API'den veri okuyamadi.")
    st.code(error_message)
    st.markdown(
        "\n".join(
            [
                "Yerel akisi tekrar kurmak icin:",
                "1. `python -m simulator --steps 2 --interval-seconds 3 --output file --file-path output/telemetry.jsonl --no-sleep`",
                "2. `python -m processor --input-file output/telemetry.jsonl --output-file output/enriched-telemetry.jsonl`",
                "3. `python -m uvicorn api.main:app --reload`",
                f"4. Dashboard'u `{base_url}` ile yenile",
            ]
        )
    )


def _render_status_banner(
    health: dict[str, object],
    summary: dict[str, object],
    auto_refresh_enabled: bool,
    refresh_interval: int,
) -> None:
    status_label = summarize_delay_label(int(summary["delayed_bus_count"]))
    refresh_label = (
        f"Otomatik yenileme: acik ({refresh_interval} sn)"
        if auto_refresh_enabled
        else "Otomatik yenileme: kapali"
    )
    st.markdown(
        f"""
        <div class="hero-banner">
          <div>
            <div class="hero-kicker">Canli Sistem Durumu</div>
            <div class="hero-title">{status_label}</div>
            <div class="hero-subtitle">
              Storage modu: <strong>{health["storage_mode"]}</strong> |
              Son veri zamani: <strong>{summary.get("latest_timestamp") or "yok"}</strong> |
              <strong>{refresh_label}</strong>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_summary_cards(summary: dict[str, object]) -> None:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Toplam Otobus", int(summary["total_buses"]))
    with col2:
        st.metric("Ortalama Hiz", f'{float(summary["average_speed_kmh"]):.1f} km/h')
    with col3:
        st.metric("Geciken Arac", int(summary["delayed_bus_count"]))
    with col4:
        st.metric(
            "Yuksek Doluluk",
            int(summary["occupancy_high_count"]),
        )


def _render_main_grid(
    lines: list[dict[str, object]],
    buses: list[dict[str, object]],
) -> None:
    left_col, right_col = st.columns([1.1, 0.9], gap="large")

    with left_col:
        st.subheader("Canli Harita")
        map_df = build_map_dataframe(buses)
        if map_df.empty:
            st.info("Secili filtrede gosterilecek otobus bulunamadi.")
        else:
            _render_map(map_df)
            st.caption(
                f"Haritada {len(map_df)} aktif otobus var. Isaretcilerin rengi doluluk seviyesini gosterir."
            )

        st.subheader("Otobus Durumlari")
        st.dataframe(
            build_bus_table_rows(buses),
            width="stretch",
            hide_index=True,
        )

    with right_col:
        st.subheader("Hat Ozetleri")
        for line in lines:
            _render_line_card(line)

        st.subheader("Secili Otobus")
        if buses:
            bus_options = {f'{bus["bus_id"]} | {bus["line_name"]}': bus for bus in buses}
            selected_label = st.selectbox("Otobus", options=list(bus_options))
            _render_bus_detail(bus_options[selected_label])
        else:
            st.info("Detay gosterilecek otobus bulunamadi.")


def _render_line_card(line: dict[str, object]) -> None:
    occupancy = (
        f'D: {line["occupancy_low_count"]} / '
        f'O: {line["occupancy_medium_count"]} / '
        f'Y: {line["occupancy_high_count"]}'
    )
    st.markdown(
        f"""
        <div class="line-card">
          <div class="line-card-header">
            <span class="line-code">{line["public_code"]}</span>
            <span class="line-name">{line["name"]}</span>
          </div>
          <div class="line-card-grid">
            <div><strong>Aktif Arac</strong><br>{line["active_bus_count"]}</div>
            <div><strong>Ort. Hiz</strong><br>{float(line["average_speed_kmh"]):.1f} km/h</div>
            <div><strong>Ort. ETA</strong><br>{int(line["average_eta_sec"])} sn</div>
            <div><strong>Geciken</strong><br>{line["delayed_bus_count"]}</div>
          </div>
          <div class="line-card-foot">Doluluk Dagilimi: {occupancy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_bus_detail(bus: dict[str, object]) -> None:
    occupancy_level = str(bus["estimated_occupancy_level"])
    badge_color = OCCUPANCY_COLORS.get(occupancy_level, "#3A86FF")
    st.markdown(
        f"""
        <div class="detail-card">
          <div class="detail-title">{bus["bus_id"]}</div>
          <div class="detail-subtitle">{bus["line_name"]} | {bus["next_stop_name"]}</div>
          <div class="detail-grid">
            <div><strong>ETA</strong><br>{bus["estimated_eta_sec"]} sn</div>
            <div><strong>Hiz</strong><br>{float(bus["speed_kmh"]):.1f} km/h</div>
            <div><strong>Binis</strong><br>{bus["boarding_count"]}</div>
            <div><strong>Tahmini Inis</strong><br>{bus["estimated_alighting_count"]}</div>
          </div>
          <div class="detail-badge" style="background:{badge_color};">
            Doluluk: {occupancy_level}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if bool(bus["is_delayed"]):
        st.warning("Bu arac gecikmeli gorunuyor.")
    else:
        st.success("Bu aracta kritik gecikme gorulmuyor.")


def _render_map(map_df) -> None:
    center_lat = float(map_df["lat"].mean())
    center_lon = float(map_df["lon"].mean())
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position="[lon, lat]",
        get_fill_color="color_rgba",
        get_line_color=[20, 52, 59, 200],
        get_radius="marker_radius",
        radius_min_pixels=8,
        radius_max_pixels=18,
        line_width_min_pixels=2,
        pickable=True,
        stroked=True,
        filled=True,
    )

    deck = pdk.Deck(
        map_style="dark",
        initial_view_state=pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=11.8,
            pitch=35,
        ),
        layers=[scatter_layer],
        tooltip={
            "html": (
                "<b>{bus_id}</b><br/>"
                "{line_name}<br/>"
                "Sonraki durak: {next_stop_name}<br/>"
                "ETA: {estimated_eta_sec} sn<br/>"
                "Doluluk: {estimated_occupancy_level}"
            ),
            "style": {
                "backgroundColor": "#14343b",
                "color": "#fefaf0",
            },
        },
    )
    st.pydeck_chart(deck, width="stretch")


def _render_stream_freshness(summary: dict[str, object]) -> None:
    latest_timestamp = str(summary.get("latest_timestamp") or "").strip()
    if not latest_timestamp:
        st.warning("Heniz canli veri gelmedi. Simulator ya da AWS akis zinciri kontrol edilmeli.")
        return

    observed_at = _parse_utc_timestamp(latest_timestamp)
    if observed_at is None:
        return

    age_seconds = int((datetime.now(timezone.utc) - observed_at).total_seconds())
    if age_seconds > 30:
        st.warning(
            (
                "Canli veri su anda guncel gorunmuyor. "
                f"Son veri yaklasik {age_seconds} sn once gelmis."
            )
        )
    else:
        st.success("Canli veri akisi guncel. Yeni konumlar dashboard'a dusuyor.")


def _parse_utc_timestamp(value: str) -> datetime | None:
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
          .stApp {
            background:
              radial-gradient(circle at top left, rgba(42,157,143,0.18), transparent 28%),
              radial-gradient(circle at top right, rgba(237,174,73,0.18), transparent 24%),
              linear-gradient(180deg, #f7f4ea 0%, #f2efe6 100%);
          }
          .stApp h1, .stApp h2, .stApp h3 {
            color: #14343b;
            letter-spacing: -0.02em;
          }
          .stApp p, .stApp label, .stApp .stCaption {
            color: #52606d;
          }
          .stApp div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(20,52,59,0.08);
            border-radius: 18px;
            padding: 0.85rem 1rem;
            box-shadow: 0 8px 24px rgba(18,52,59,0.08);
          }
          .stApp div[data-testid="stMetricLabel"] p {
            color: #52606d;
            font-weight: 600;
          }
          .stApp div[data-testid="stMetricValue"] {
            color: #14343b;
          }
          .stApp div[data-testid="stMetricDelta"] {
            color: #5c677d;
          }
          .stApp div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 22px rgba(18,52,59,0.08);
          }
          section[data-testid="stSidebar"] h1,
          section[data-testid="stSidebar"] h2,
          section[data-testid="stSidebar"] h3,
          section[data-testid="stSidebar"] label,
          section[data-testid="stSidebar"] p,
          section[data-testid="stSidebar"] .stCaption {
            color: #eef4f5;
          }
          .hero-banner {
            background: linear-gradient(135deg, #12343b 0%, #1b4d59 100%);
            padding: 1.1rem 1.2rem;
            border-radius: 18px;
            color: #fefaf0;
            margin-bottom: 1rem;
            box-shadow: 0 12px 30px rgba(18,52,59,0.18);
          }
          .hero-kicker {
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.8rem;
            opacity: 0.85;
          }
          .hero-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 0.2rem;
          }
          .hero-subtitle {
            margin-top: 0.3rem;
            opacity: 0.9;
          }
          .line-card, .detail-card {
            background: rgba(255,255,255,0.86);
            border: 1px solid rgba(18,52,59,0.08);
            border-radius: 18px;
            padding: 1rem 1rem 0.9rem 1rem;
            margin-bottom: 0.85rem;
            box-shadow: 0 10px 22px rgba(18,52,59,0.08);
          }
          .line-card-header {
            display: flex;
            gap: 0.65rem;
            align-items: baseline;
            margin-bottom: 0.8rem;
          }
          .line-code {
            font-size: 1.4rem;
            font-weight: 800;
            color: #1d3557;
          }
          .line-name {
            font-size: 0.95rem;
            color: #264653;
          }
          .line-card-grid, .detail-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.7rem 0.8rem;
          }
          .line-card-foot {
            margin-top: 0.85rem;
            color: #4f5d75;
            font-size: 0.9rem;
          }
          .detail-title {
            font-size: 1.25rem;
            font-weight: 800;
            color: #1d3557;
          }
          .detail-subtitle {
            color: #5c677d;
            margin-bottom: 0.8rem;
          }
          .detail-badge {
            display: inline-block;
            margin-top: 0.8rem;
            padding: 0.45rem 0.75rem;
            border-radius: 999px;
            color: white;
            font-weight: 700;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
