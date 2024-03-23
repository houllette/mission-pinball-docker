import os
from mpfmc.tests.FullMpfMachineTestCase import FullMachineTestCase


class TestSimpleGame(FullMachineTestCase):

    def get_machine_path(self):
        return os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))

    def test_single_player_game(self):
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(.1)
        # game should be running
        self.assertIsNotNone(self.machine.game)
        self.assertEqual(1, self.machine.game.player.ball)
        # playfield expects a ball
        self.assertEqual(1, self.machine.playfield.available_balls)
        # but its not there yet
        self.assertEqual(0, self.machine.playfield.balls)

        self.advance_time_and_run(3)
        # player presses eject
        self.hit_and_release_switch("s_ball_launch")

        # after 3 its there
        self.advance_time_and_run(2)
        self.hit_and_release_switch("s_right_ramp_enter")
        self.advance_time_and_run(1)
        self.assertEqual(1, self.machine.playfield.balls)

        self.assertTextOnTopSlide("BALL 1    FREE PLAY")

        # make some points
        self.hit_and_release_switch("s_left_jet")
        self.hit_and_release_switch("s_left_jet")
        self.hit_and_release_switch("s_left_jet")
        self.hit_and_release_switch("s_left_jet")
        self.advance_time_and_run()
        self.assertEqual(4 * 75020, self.machine.game.player.score)
        self.assertTextOnTopSlide("300,080")

        # test the claw
        self.hit_switch_and_run("s_elevator_hold", 1)
        self.assertEqual("enabled", self.machine.coils["c_claw_motor_right"].hw_driver.state)

        self.hit_switch_and_run("s_claw_position_1", 1)
        self.assertEqual("disabled", self.machine.coils["c_claw_motor_right"].hw_driver.state)

        self.assertEqual("enabled", self.machine.coils["c_elevator_motor"].hw_driver.state)
        self.assertEqual("enabled", self.machine.coils["c_claw_magnet"].hw_driver.state)
        self.hit_switch_and_run("s_elevator_index", 1)
        self.release_switch_and_run("s_elevator_hold", 1)

        self.assertEqual("disabled", self.machine.coils["c_elevator_motor"].hw_driver.state)
        self.assertEqual("enabled", self.machine.coils["c_claw_magnet"].hw_driver.state)

        self.hit_switch_and_run("s_flipper_lower_left", 1)
        self.assertEqual("enabled", self.machine.coils["c_claw_motor_left"].hw_driver.state)
        self.assertEqual("disabled", self.machine.coils["c_claw_motor_right"].hw_driver.state)

        self.hit_and_release_switch("s_ball_launch")
        self.advance_time_and_run()
        self.assertEqual("disabled", self.machine.coils["c_claw_magnet"].hw_driver.state)
        self.assertEqual("disabled", self.machine.coils["c_claw_motor_left"].hw_driver.state)
        self.assertEqual("disabled", self.machine.coils["c_claw_motor_right"].hw_driver.state)

        self.release_switch_and_run("s_flipper_lower_left", 1)

        # ball drains
        self.machine.default_platform.add_ball_to_device(self.machine.ball_devices.trough)
        # wait for highscore display
        self.advance_time_and_run(10)
        self.assertEqual(0, self.machine.playfield.balls)
        self.assertEqual(2, self.machine.game.player.ball)

        self.advance_time_and_run(5)
        # player presses eject
        self.hit_and_release_switch("s_ball_launch")

        # and it should eject a new ball to the pf
        self.advance_time_and_run(2)
        self.hit_and_release_switch("s_right_ramp_enter")
        self.advance_time_and_run(1)
        self.assertEqual(1, self.machine.playfield.balls)

        # ball drains again
        self.machine.default_platform.add_ball_to_device(self.machine.ball_devices.trough)
        # wait for highscore display
        self.advance_time_and_run(10)
        self.assertEqual(0, self.machine.playfield.balls)
        self.assertEqual(3, self.machine.game.player.ball)

        self.advance_time_and_run(5)
        # player presses eject
        self.hit_and_release_switch("s_ball_launch")

        # and it should eject a new ball to the pf
        self.advance_time_and_run(2)
        self.hit_and_release_switch("s_right_ramp_enter")
        self.advance_time_and_run(1)
        self.assertEqual(1, self.machine.playfield.balls)

        # ball drains again. game should end
        self.machine.default_platform.add_ball_to_device(self.machine.ball_devices.trough)
        self.advance_time_and_run(10)

        self.mock_event('text_input_high_score_complete')

        # enter high score
        self.assertSlideOnTop("high_score_enter_initials")
        self.hit_and_release_switch("s_flipper_lower_right")
        self.hit_and_release_switch("s_flipper_lower_right")
        self.hit_and_release_switch("s_start")  # C
        self.advance_time_and_run()
        self.assertTextOnTopSlide("C")
        self.hit_and_release_switch("s_flipper_lower_right")
        self.hit_and_release_switch("s_start")  # CD
        self.advance_time_and_run()
        self.assertTextOnTopSlide("CD")
        self.hit_and_release_switch("s_flipper_lower_right")
        self.hit_and_release_switch("s_start")  # CDE
        self.advance_time_and_run()
        self.assertTextOnTopSlide("CDE")
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run()

        self.assertEventCalled('text_input_high_score_complete')
        self.advance_time_and_run(10)
        self.assertIsNone(self.machine.game)
