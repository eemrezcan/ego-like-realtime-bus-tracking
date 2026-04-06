from __future__ import annotations

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
        "Sentetik telemetri, MQTT akisi, bulutta isleme ve canli izleme zincirinin lokal demo ekrani."
    )

    with st.sidebar:
        st.header("Baglanti")
        base_url = st.text_input("API Base URL", value=settings.api_base_url)
        selected_line_default = settings.default_selected_line or "Tum Hatlar"
        refresh_requested = st.button("Veriyi Yenile", use_container_width=True)
        st.caption("API ayakta ise kartlar ve harita bu veri kaynagindan beslenir.")

    client = DashboardApiClient(base_url=base_url)

    if refresh_requested:
        st.cache_data.clear()

    try:
        health = _get_health(base_url)
        summary = _get_summary(base_url)
        lines = _get_lines(base_url)
        buses = _get_buses(base_url)
    except DashboardApiError as exc:
        _render_unavailable_state(base_url, str(exc))
        return

    line_options = ["Tum Hatlar"] + [line["line_id"] for line in lines]
    selected_line = st.sidebar.selectbox(
        "Hat Filtresi",
        options=line_options,
        index=line_options.index(selected_line_default)
        if selected_line_default in line_options
        else 0,
    )
    filtered_buses = filter_buses_by_line(buses, selected_line)

    _render_status_banner(health, summary)
    _render_summary_cards(summary)
    _render_main_grid(lines, filtered_buses)


@st.cache_data(ttl=10)
def _get_health(base_url: str) -> dict[str, object]:
    return DashboardApiClient(base_url=base_url).get_health()


@st.cache_data(ttl=10)
def _get_summary(base_url: str) -> dict[str, object]:
    return DashboardApiClient(base_url=base_url).get_summary()


@st.cache_data(ttl=10)
def _get_lines(base_url: str) -> list[dict[str, object]]:
    return DashboardApiClient(base_url=base_url).get_lines()


@st.cache_data(ttl=10)
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
) -> None:
    status_label = summarize_delay_label(int(summary["delayed_bus_count"]))
    st.markdown(
        f"""
        <div class="hero-banner">
          <div>
            <div class="hero-kicker">Canli Sistem Durumu</div>
            <div class="hero-title">{status_label}</div>
            <div class="hero-subtitle">
              Storage modu: <strong>{health["storage_mode"]}</strong> |
              Son veri zamani: <strong>{summary.get("latest_timestamp") or "yok"}</strong>
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
            st.map(map_df[["lat", "lon"]], use_container_width=True)
            st.caption("Harita noktalarinin sirasi secili filtredeki guncel otobus durumuna gore olusturulur.")

        st.subheader("Otobus Durumlari")
        st.dataframe(
            build_bus_table_rows(buses),
            use_container_width=True,
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
