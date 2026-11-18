import pytest

from osdagbridge.core.reports.report_generator import ReportDataBridge


@pytest.mark.parametrize(
    ("diaphragm", "prefix"),
    [(False, "crossbracing"), (True, "end_diaphragm")],
)
def test_transverse_checks_read_only_member_results(diaphragm, prefix):
    """The desktop drawings dialog can add text labels to a design pair."""
    outputs = {
        f"{prefix}_design_results": {
            "G1-G2": {
                "diagonal": {"compression": {"Member.tension_capacity": 20.0}},
                "chord": {"tension": {"Member.tension_capacity": 40.0}},
                "ed_type": "Cross Bracing",
                "ed_bracing_type": "X-Bracing",
            },
        },
        f"{prefix}_forces_dict": {
            "pairs": {
                "G1-G2": {"diag_compression_kN": 5.0, "diag_compression_gov_lc": "ULS"},
            },
        },
    }

    bridge = ReportDataBridge(outputs, {}, None)
    results = list(bridge.transverse_checks("compression", diaphragm=diaphragm))

    assert len(results) == 1
    assert results[0]["capacity_kN"] == 20.0
    assert results[0]["demand_kN"] == 5.0
    assert results[0]["load_combination"] == "ULS"
