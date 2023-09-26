# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.base import PowerfactorDirection
from psdm.steadystate_case.characteristic import Characteristic
from psdm.steadystate_case.controller import (
    ControlCosphiConst,
    ControlCosphiP,
    ControlCosphiU,
    ControlPConst,
    ControlPF,
    ControlledVoltageRef,
    ControlQConst,
    ControlQP,
    ControlQU,
    ControlTanphiConst,
    ControlUConst,
)


class TestControlQConst:
    @pytest.mark.parametrize(
        (
            "value",
            "value_a",
            "value_b",
            "value_c",
            "is_symmetrical",
            "expectation",
        ),
        [
            (-1500, -500, -500, -500, True, does_not_raise()),
            (-1500, -500, -500, -500, False, pytest.raises(pydantic.ValidationError)),
            (1500, 500, 500, 500, True, does_not_raise()),
            (1500, 600, 500, 500, True, pytest.raises(pydantic.ValidationError)),
            (1500, 500, 1000, 0, False, does_not_raise()),
            (1700, 500, 1000, 200, True, pytest.raises(pydantic.ValidationError)),
            (1700, 500, 1000, 100, False, pytest.raises(pydantic.ValidationError)),
            (0, 0, 0, 0, True, does_not_raise()),
            (None, None, None, None, None, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        value,
        value_a,
        value_b,
        value_c,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            ControlQConst(
                value=value,
                value_a=value_a,
                value_b=value_b,
                value_c=value_c,
                is_symmetrical=is_symmetrical,
            )


class TestControlUConst:
    @pytest.mark.parametrize(
        (
            "u_set",
            "u_meas_ref",
            "expectation",
        ),
        [
            (110000, ControlledVoltageRef.POS_SEQ, does_not_raise()),
            (100000, ControlledVoltageRef.AVG, does_not_raise()),
            (110000, None, pytest.raises(pydantic.ValidationError)),
            (
                -110000,
                ControlledVoltageRef.POS_SEQ,
                pytest.raises(pydantic.ValidationError),
            ),
            (None, ControlledVoltageRef.POS_SEQ, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        u_set,
        u_meas_ref,
        expectation,
    ) -> None:
        with expectation:
            ControlUConst(
                u_set=u_set,
                u_meas_ref=u_meas_ref,
            )


class TestControlTanphiConst:
    @pytest.mark.parametrize(
        (
            "tanphi_dir",
            "tanphi",
            "tanphi_a",
            "tanphi_b",
            "tanphi_c",
            "is_symmetrical",
            "expectation",
        ),
        [
            (PowerfactorDirection.UE, 1, 1, 1, 1, True, does_not_raise()),
            (PowerfactorDirection.UE, 0, 0, 0, 0, True, does_not_raise()),
            (PowerfactorDirection.OE, 0.9, 0.9, 0.9, 0.9, True, does_not_raise()),
            (PowerfactorDirection.OE, 0.9, 0.9, 0.8, 1, False, does_not_raise()),
            (PowerfactorDirection.OE, 0.9, 0.6, 0.9, 0.9, True, pytest.raises(pydantic.ValidationError)),
            (PowerfactorDirection.OE, -0.9, -0.9, -0.9, -0.9, True, pytest.raises(pydantic.ValidationError)),
            (PowerfactorDirection.OE, 0.9, -0.9, 0.9, 0.9, True, pytest.raises(pydantic.ValidationError)),
            (PowerfactorDirection.OE, 0.9, -0.6, 0.9, 0.9, False, pytest.raises(pydantic.ValidationError)),
            (PowerfactorDirection.OE, 2, 2, 2, 2, True, pytest.raises(pydantic.ValidationError)),
            (PowerfactorDirection.OE, None, None, None, None, True, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        tanphi_dir,
        tanphi,
        tanphi_a,
        tanphi_b,
        tanphi_c,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            ControlTanphiConst(
                tanphi_dir=tanphi_dir,
                value=tanphi,
                value_a=tanphi_a,
                value_b=tanphi_b,
                value_c=tanphi_c,
                is_symmetrical=is_symmetrical,
            )


class TestControlCosphiConst:
    @pytest.mark.parametrize(
        (
            "cosphi_dir",
            "cosphi",
            "cosphi_a",
            "cosphi_b",
            "cosphi_c",
            "is_symmetrical",
            "expectation",
        ),
        [
            (PowerfactorDirection.UE, 1, 1, 1, 1, True, does_not_raise()),
            (PowerfactorDirection.UE, 0, 0, 0, 0, True, does_not_raise()),
            (PowerfactorDirection.OE, 0.9, 0.9, 0.9, 0.9, True, does_not_raise()),
            (PowerfactorDirection.OE, 0.9, 0.9, 0.8, 1, False, does_not_raise()),
            (PowerfactorDirection.OE, 0.9, 0.6, 0.9, 0.9, True, pytest.raises(pydantic.ValidationError)),
            (PowerfactorDirection.OE, -0.9, -0.9, -0.9, -0.9, True, pytest.raises(pydantic.ValidationError)),
            (PowerfactorDirection.OE, 0.9, -0.9, 0.9, 0.9, True, pytest.raises(pydantic.ValidationError)),
            (PowerfactorDirection.OE, 0.9, -0.6, 0.9, 0.9, False, pytest.raises(pydantic.ValidationError)),
            (PowerfactorDirection.OE, 2, 2, 2, 2, True, pytest.raises(pydantic.ValidationError)),
            (PowerfactorDirection.OE, None, None, None, None, True, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        cosphi_dir,
        cosphi,
        cosphi_a,
        cosphi_b,
        cosphi_c,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            ControlCosphiConst(
                cosphi_dir=cosphi_dir,
                value=cosphi,
                value_a=cosphi_a,
                value_b=cosphi_b,
                value_c=cosphi_c,
                is_symmetrical=is_symmetrical,
            )


class TestControlCosphiP:
    @pytest.mark.parametrize(
        (
            "cosphi_ue",
            "cosphi_oe",
            "p_threshold_ue",
            "p_threshold_oe",
            "expectation",
        ),
        [
            (0.9, 0.9, -1, -2, does_not_raise()),
            (1, 0, -2, -1, does_not_raise()),
            (0.9, 1.1, -2, -1, pytest.raises(pydantic.ValidationError)),
            (1.1, 0.9, -2, -1, pytest.raises(pydantic.ValidationError)),
            (-0.9, 0.9, -2, -1, pytest.raises(pydantic.ValidationError)),
            (0.9, -0.9, -2, -1, pytest.raises(pydantic.ValidationError)),
            (0.9, 0.9, 2, -1, pytest.raises(pydantic.ValidationError)),
            (0.9, 0.9, -2, 1, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(  # noqa: PLR0913
        self,
        cosphi_ue,
        cosphi_oe,
        p_threshold_ue,
        p_threshold_oe,
        expectation,
    ) -> None:
        with expectation:
            ControlCosphiP(
                cosphi_ue=cosphi_ue,
                cosphi_oe=cosphi_oe,
                p_threshold_ue=p_threshold_ue,
                p_threshold_oe=p_threshold_oe,
            )


class TestControlCosphiU:
    @pytest.mark.parametrize(
        (
            "cosphi_ue",
            "cosphi_oe",
            "u_threshold_ue",
            "u_threshold_oe",
            "expectation",
        ),
        [
            (0.9, 0.9, 20000, 24000, does_not_raise()),
            (1, 0, 24000, 20000, does_not_raise()),
            (0.9, 1.1, 24000, 20000, pytest.raises(pydantic.ValidationError)),
            (1.1, 0.9, 24000, 20000, pytest.raises(pydantic.ValidationError)),
            (-0.9, 0.9, 24000, 20000, pytest.raises(pydantic.ValidationError)),
            (0.9, -0.9, 24000, 20000, pytest.raises(pydantic.ValidationError)),
            (0.9, 0.9, -24000, 20000, pytest.raises(pydantic.ValidationError)),
            (0.9, 0.9, 20000, -20000, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(  # noqa: PLR0913
        self,
        cosphi_ue,
        cosphi_oe,
        u_threshold_ue,
        u_threshold_oe,
        expectation,
    ) -> None:
        with expectation:
            ControlCosphiU(
                cosphi_ue=cosphi_ue,
                cosphi_oe=cosphi_oe,
                u_threshold_ue=u_threshold_ue,
                u_threshold_oe=u_threshold_oe,
            )


class TestControlQU:
    @pytest.mark.parametrize(
        (
            "droop_tg_2015",
            "droop_tg_2018",
            "u_q0",
            "u_deadband_up",
            "u_deadband_low",
            "q_max_ue",
            "q_max_oe",
            "expectation",
        ),
        [
            (5, 6, 110000, 1000, 1000, 10000, 10000, does_not_raise()),
            (5, 6, 110000, 1000, 2000, 20000, 10000, does_not_raise()),
            (-5, 6, 110000, 1000, 2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, -6, 110000, 1000, 2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, -110000, 1000, 2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, -1000, 2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, 1000, -2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, 1000, 2000, -20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, 1000, 2000, 20000, -10000, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(  # noqa: PLR0913
        self,
        droop_tg_2015,
        droop_tg_2018,
        u_q0,
        u_deadband_up,
        u_deadband_low,
        q_max_ue,
        q_max_oe,
        expectation,
    ) -> None:
        with expectation:
            ControlQU(
                droop_tg_2015=droop_tg_2015,
                droop_tg_2018=droop_tg_2018,
                u_q0=u_q0,
                u_deadband_up=u_deadband_up,
                u_deadband_low=u_deadband_low,
                q_max_ue=q_max_ue,
                q_max_oe=q_max_oe,
            )


class TestControlQP:
    @pytest.mark.parametrize(
        (
            "q_p_characteristic",
            "q_max_ue",
            "q_max_oe",
            "expectation",
        ),
        [
            (Characteristic(name="Q_P_Char"), 10000, 10000, does_not_raise()),
            (Characteristic(name="Q_P_Char"), 10000, 20000, does_not_raise()),
            (None, 10000, 10000, pytest.raises(pydantic.ValidationError)),
            (Characteristic(name="Q_P_Char"), -10000, 10000, pytest.raises(pydantic.ValidationError)),
            (Characteristic(name="Q_P_Char"), 10000, -10000, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(  # noqa: PLR0913
        self,
        q_p_characteristic,
        q_max_ue,
        q_max_oe,
        expectation,
    ) -> None:
        with expectation:
            ControlQP(
                q_p_characteristic=q_p_characteristic,
                q_max_ue=q_max_ue,
                q_max_oe=q_max_oe,
            )


class TestControlPF:
    @pytest.mark.parametrize(
        (
            "droop_over_freq",
            "droop_under_freq",
            "f_p0",
            "f_deadband_up",
            "f_deadband_low",
            "expectation",
        ),
        [
            (40, 40, 50, 0.2, 0.2, does_not_raise()),
            (-40, 40, 50, 0.2, 0.2, pytest.raises(pydantic.ValidationError)),
            (40, -40, 50, 0.2, 0.2, pytest.raises(pydantic.ValidationError)),
            (40, 40, -50, 0.2, 0.2, pytest.raises(pydantic.ValidationError)),
            (40, 40, 50, -0.2, 0.2, pytest.raises(pydantic.ValidationError)),
            (40, 40, 50, 0.2, -0.2, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(  # noqa: PLR0913
        self,
        droop_over_freq,
        droop_under_freq,
        f_p0,
        f_deadband_up,
        f_deadband_low,
        expectation,
    ) -> None:
        with expectation:
            ControlPF(
                droop_over_freq=droop_over_freq,
                droop_under_freq=droop_under_freq,
                f_p0=f_p0,
                f_deadband_up=f_deadband_up,
                f_deadband_low=f_deadband_low,
            )


class TestControlPConst:
    @pytest.mark.parametrize(
        (
            "value",
            "value_a",
            "value_b",
            "value_c",
            "is_symmetrical",
            "expectation",
        ),
        [
            (-1500, -500, -500, -500, True, does_not_raise()),
            (-1500, -500, -500, -500, False, pytest.raises(pydantic.ValidationError)),
            (1500, 500, 500, 500, True, does_not_raise()),
            (1500, 600, 500, 500, True, pytest.raises(pydantic.ValidationError)),
            (1500, 500, 1000, 0, False, does_not_raise()),
            (1700, 500, 1000, 200, True, pytest.raises(pydantic.ValidationError)),
            (1700, 500, 1000, 100, False, pytest.raises(pydantic.ValidationError)),
            (0, 0, 0, 0, True, does_not_raise()),
            (None, None, None, None, None, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        value,
        value_a,
        value_b,
        value_c,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            ControlPConst(
                value=value,
                value_a=value_a,
                value_b=value_b,
                value_c=value_c,
                is_symmetrical=is_symmetrical,
            )
