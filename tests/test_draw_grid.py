import unittest
from unittest.mock import Mock, patch, call
import turtle
from turtlegridutil.core import draw_grid


class TestDrawGrid(unittest.TestCase):
    def setUp(self):
        self.mock_screen = Mock(spec=turtle.Screen())
        self.mock_screen.window_width.return_value = 800
        self.mock_screen.window_height.return_value = 600

    def test_draw_grid_default_parameters(self):
        with patch('turtle.Turtle') as mock_turtle:
            draw_grid(self.mock_screen)

            # Check if screen methods are called correctly
            self.mock_screen.tracer.assert_any_call(0)
            self.mock_screen.update.assert_called_once()
            self.mock_screen.tracer.assert_called_with(1)

            # Check if Turtle is created and configured correctly
            mock_turtle.assert_called_once()
            mock_turtle_instance = mock_turtle.return_value
            mock_turtle_instance.hideturtle.assert_called_once()

            # Check major line drawing
            mock_turtle_instance.pensize.assert_any_call(1)
            mock_turtle_instance.pencolor.assert_any_call("black")

            # Check scale drawing
            mock_turtle_instance.color.assert_called_with("black")
            mock_turtle_instance.write.assert_called()
            mock_turtle_instance.dot.assert_called_with(5)

            # Verify number of calls for major lines and scale
            self.assertEqual(mock_turtle_instance.penup.call_count, 28)
            self.assertEqual(mock_turtle_instance.pendown.call_count, 28)
            self.assertEqual(mock_turtle_instance.goto.call_count, 42)

    def test_draw_grid_custom_major_line_step(self):
        with patch('turtle.Turtle') as mock_turtle:
            draw_grid(self.mock_screen, major_line_step=50)

            # Check if screen methods are called correctly
            self.mock_screen.tracer.assert_any_call(0)
            self.mock_screen.update.assert_called_once()
            self.mock_screen.tracer.assert_called_with(1)

            # Check if Turtle is created and configured correctly
            mock_turtle.assert_called_once()
            mock_turtle_instance = mock_turtle.return_value
            mock_turtle_instance.hideturtle.assert_called_once()

            # Check major line drawing with custom step
            mock_turtle_instance.pensize.assert_any_call(1)
            mock_turtle_instance.pencolor.assert_any_call("black")

            # Verify number of calls for major lines (should be more than default)
            self.assertGreater(mock_turtle_instance.penup.call_count, 16)
            self.assertGreater(mock_turtle_instance.pendown.call_count, 16)
            self.assertGreater(mock_turtle_instance.goto.call_count, 32)

            # Check scale drawing
            mock_turtle_instance.color.assert_called_with("black")
            mock_turtle_instance.write.assert_called()
            mock_turtle_instance.dot.assert_called_with(5)

            # Verify that the scale step matches the custom major line step
            scale_calls = [call for call in mock_turtle_instance.method_calls if
                           call[0] == 'goto' and call[1][0] % 50 == 0]
            self.assertGreater(len(scale_calls), 0)

    def test_draw_grid_custom_minor_line_step(self):
        with patch('turtle.Turtle') as mock_turtle:
            draw_grid(self.mock_screen, minor_line_step=25)

            # Check if screen methods are called correctly
            self.mock_screen.tracer.assert_any_call(0)
            self.mock_screen.update.assert_called_once()
            self.mock_screen.tracer.assert_called_with(1)

            # Check if Turtle is created and configured correctly
            mock_turtle.assert_called_once()
            mock_turtle_instance = mock_turtle.return_value
            mock_turtle_instance.hideturtle.assert_called_once()

            # Check minor line drawing with custom step
            mock_turtle_instance.pensize.assert_any_call(1)
            mock_turtle_instance.pencolor.assert_any_call("gray")

            # Verify number of calls for minor lines (should be more than major lines)
            minor_line_calls = [call for call in mock_turtle_instance.method_calls if
                                call[0] == 'goto' and (call[1][0] % 25 == 0 or call[1][1] % 25 == 0)]
            major_line_calls = [call for call in mock_turtle_instance.method_calls if
                                call[0] == 'goto' and (call[1][0] % 100 == 0 or call[1][1] % 100 == 0)]
            self.assertGreaterEqual(len(minor_line_calls), len(major_line_calls))

            # Check major line drawing
            mock_turtle_instance.pensize.assert_any_call(1)
            mock_turtle_instance.pencolor.assert_any_call("black")

            # Check scale drawing
            mock_turtle_instance.color.assert_called_with("black")
            mock_turtle_instance.write.assert_called()
            mock_turtle_instance.dot.assert_called_with(5)

            # Verify that the scale step matches the default major line step
            scale_calls = [call for call in mock_turtle_instance.method_calls if
                           call[0] == 'goto' and call[1][0] % 100 == 0 and call[1][1] == 0]
            self.assertGreater(len(scale_calls), 0)

    def test_draw_grid_custom_line_colors(self):
        with patch('turtle.Turtle') as mock_turtle:
            custom_major_color = "red"
            custom_minor_color = "blue"
            draw_grid(self.mock_screen, major_line_color=custom_major_color, minor_line_color=custom_minor_color,
                      minor_line_step=25)

            # Check if screen methods are called correctly
            self.mock_screen.tracer.assert_any_call(0)
            self.mock_screen.update.assert_called_once()
            self.mock_screen.tracer.assert_called_with(1)

            # Check if Turtle is created and configured correctly
            mock_turtle.assert_called_once()
            mock_turtle_instance = mock_turtle.return_value
            mock_turtle_instance.hideturtle.assert_called_once()

            # Check minor line drawing with custom color
            mock_turtle_instance.pencolor.assert_any_call(custom_minor_color)

            # Check major line drawing with custom color
            mock_turtle_instance.pencolor.assert_any_call(custom_major_color)

            # Verify that both colors were used
            pencolor_calls = [call for call in mock_turtle_instance.method_calls if call[0] == 'pencolor']
            self.assertIn(call.pencolor(custom_minor_color), pencolor_calls)
            self.assertIn(call.pencolor(custom_major_color), pencolor_calls)

            # Check that minor lines were drawn
            minor_line_calls = [call for call in mock_turtle_instance.method_calls if
                                call[0] == 'goto' and (call[1][0] % 25 == 0 or call[1][1] % 25 == 0)]
            self.assertGreater(len(minor_line_calls), 0)

            # Check that major lines were drawn
            major_line_calls = [call for call in mock_turtle_instance.method_calls if
                                call[0] == 'goto' and (call[1][0] % 100 == 0 or call[1][1] % 100 == 0)]
            self.assertGreater(len(major_line_calls), 0)

            # Check scale drawing
            mock_turtle_instance.color.assert_called_with("black")
            mock_turtle_instance.write.assert_called()
            mock_turtle_instance.dot.assert_called_with(5)

    def test_draw_grid_custom_line_widths(self):
        with patch('turtle.Turtle') as mock_turtle:
            custom_major_width = 3
            custom_minor_width = 2
            draw_grid(self.mock_screen, major_line_width=custom_major_width, minor_line_width=custom_minor_width,
                      minor_line_step=25)

            # Check if screen methods are called correctly
            self.mock_screen.tracer.assert_any_call(0)
            self.mock_screen.update.assert_called_once()
            self.mock_screen.tracer.assert_called_with(1)

            # Check if Turtle is created and configured correctly
            mock_turtle.assert_called_once()
            mock_turtle_instance = mock_turtle.return_value
            mock_turtle_instance.hideturtle.assert_called_once()

            # Check minor line drawing with custom width
            mock_turtle_instance.pensize.assert_any_call(custom_minor_width)
            mock_turtle_instance.pencolor.assert_any_call("gray")

            # Check major line drawing with custom width
            mock_turtle_instance.pensize.assert_any_call(custom_major_width)
            mock_turtle_instance.pencolor.assert_any_call("black")

            # Verify that both widths were used
            pensize_calls = [call for call in mock_turtle_instance.method_calls if call[0] == 'pensize']
            self.assertIn(call.pensize(custom_minor_width), pensize_calls)
            self.assertIn(call.pensize(custom_major_width), pensize_calls)

            # Check that minor lines were drawn
            minor_line_calls = [call for call in mock_turtle_instance.method_calls if
                                call[0] == 'goto' and (call[1][0] % 25 == 0 or call[1][1] % 25 == 0)]
            self.assertGreater(len(minor_line_calls), 0)

            # Check that major lines were drawn
            major_line_calls = [call for call in mock_turtle_instance.method_calls if
                                call[0] == 'goto' and (call[1][0] % 100 == 0 or call[1][1] % 100 == 0)]
            self.assertGreater(len(major_line_calls), 0)

            # Check scale drawing
            mock_turtle_instance.color.assert_called_with("black")
            mock_turtle_instance.write.assert_called()
            mock_turtle_instance.dot.assert_called_with(5)

    def test_draw_grid_without_scale(self):
        with patch('turtle.Turtle') as mock_turtle:
            draw_grid(self.mock_screen, use_scale=False)

            # Check if screen methods are called correctly
            self.mock_screen.tracer.assert_any_call(0)
            self.mock_screen.update.assert_called_once()
            self.mock_screen.tracer.assert_called_with(1)

            # Check if Turtle is created and configured correctly
            mock_turtle.assert_called_once()
            mock_turtle_instance = mock_turtle.return_value
            mock_turtle_instance.hideturtle.assert_called_once()

            # Check major line drawing
            mock_turtle_instance.pensize.assert_any_call(1)
            mock_turtle_instance.pencolor.assert_any_call("black")

            # Verify that scale is not drawn
            mock_turtle_instance.write.assert_not_called()
            mock_turtle_instance.dot.assert_not_called()

            # Verify number of calls for major lines
            self.assertEqual(mock_turtle_instance.penup.call_count, 14)
            self.assertEqual(mock_turtle_instance.pendown.call_count, 14)
            self.assertEqual(mock_turtle_instance.goto.call_count, 28)

            # Verify that color is not set for scale drawing
            mock_turtle_instance.color.assert_not_called()

    def test_draw_grid_custom_scale_step(self):
        with patch('turtle.Turtle') as mock_turtle:
            custom_scale_step = 75
            draw_grid(self.mock_screen, scale_step=custom_scale_step)

            # Check if screen methods are called correctly
            self.mock_screen.tracer.assert_any_call(0)
            self.mock_screen.update.assert_called_once()
            self.mock_screen.tracer.assert_called_with(1)

            # Check if Turtle is created and configured correctly
            mock_turtle.assert_called_once()
            mock_turtle_instance = mock_turtle.return_value
            mock_turtle_instance.hideturtle.assert_called_once()

            # Check major line drawing
            mock_turtle_instance.pensize.assert_any_call(1)
            mock_turtle_instance.pencolor.assert_any_call("black")

            # Check scale drawing with custom step
            mock_turtle_instance.color.assert_called_with("black")
            mock_turtle_instance.write.assert_called()
            mock_turtle_instance.dot.assert_called_with(5)

            # Verify that the scale step matches the custom scale step
            scale_calls = [call for call in mock_turtle_instance.method_calls if
                           call[0] == 'goto' and (
                                       call[1][0] % custom_scale_step == 0 or call[1][1] % custom_scale_step == 0)]
            self.assertGreater(len(scale_calls), 0)

            # Verify that the custom scale step is used instead of the default major line step
            default_major_step_calls = [call for call in mock_turtle_instance.method_calls if
                                        call[0] == 'goto' and (call[1][0] % 100 == 0 and call[1][1] % 100 == 0)]
            self.assertGreater(len(scale_calls), len(default_major_step_calls))

    def test_draw_grid_custom_font_settings(self):
        with patch('turtle.Turtle') as mock_turtle:
            custom_font_color = "blue"
            custom_font_family = "Times New Roman"
            custom_font_size = 18
            custom_font_style = "bold"
            draw_grid(self.mock_screen, font_color=custom_font_color, font_family=custom_font_family,
                      font_size=custom_font_size, font_style=custom_font_style)

            # Check if screen methods are called correctly
            self.mock_screen.tracer.assert_any_call(0)
            self.mock_screen.update.assert_called_once()
            self.mock_screen.tracer.assert_called_with(1)

            # Check if Turtle is created and configured correctly
            mock_turtle.assert_called_once()
            mock_turtle_instance = mock_turtle.return_value
            mock_turtle_instance.hideturtle.assert_called_once()

            # Check major line drawing
            mock_turtle_instance.pensize.assert_any_call(1)
            mock_turtle_instance.pencolor.assert_any_call("black")

            # Check scale drawing with custom font settings
            mock_turtle_instance.color.assert_called_with(custom_font_color)
            mock_turtle_instance.write.assert_called()

            # Verify that the custom font settings are used
            write_calls = [call for call in mock_turtle_instance.method_calls if call[0] == 'write']
            self.assertTrue(any(
                call[2].get('font') == (custom_font_family, custom_font_size, custom_font_style) for call in
                write_calls))

            # Check that scale points are drawn
            mock_turtle_instance.dot.assert_called_with(5)

            # Verify number of calls for major lines and scale
            self.assertGreater(mock_turtle_instance.penup.call_count, 0)
            self.assertGreater(mock_turtle_instance.pendown.call_count, 0)
            self.assertGreater(mock_turtle_instance.goto.call_count, 0)

    def test_draw_grid_scale_points_size_zero(self):
        with patch('turtle.Turtle') as mock_turtle:
            draw_grid(self.mock_screen, scale_points_size=0)

            # Check if screen methods are called correctly
            self.mock_screen.tracer.assert_any_call(0)
            self.mock_screen.update.assert_called_once()
            self.mock_screen.tracer.assert_called_with(1)

            # Check if Turtle is created and configured correctly
            mock_turtle.assert_called_once()
            mock_turtle_instance = mock_turtle.return_value
            mock_turtle_instance.hideturtle.assert_called_once()

            # Check major line drawing
            mock_turtle_instance.pensize.assert_any_call(1)
            mock_turtle_instance.pencolor.assert_any_call("black")

            # Check scale drawing
            mock_turtle_instance.color.assert_called_with("black")
            mock_turtle_instance.write.assert_called()

            # Verify that dot() method is not called when scale_points_size is 0
            dot_calls = [call for call in mock_turtle_instance.method_calls if call[0] == 'dot']
            self.assertEqual(len(dot_calls), 0)

            # Verify number of calls for major lines and scale
            self.assertGreater(mock_turtle_instance.penup.call_count, 0)
            self.assertGreater(mock_turtle_instance.pendown.call_count, 0)
            self.assertGreater(mock_turtle_instance.goto.call_count, 0)

    def test_draw_grid_odd_dimensions(self):
        with patch('turtle.Turtle') as mock_turtle:
            # Set up a mock screen with odd dimensions
            self.mock_screen.window_width.return_value = 801
            self.mock_screen.window_height.return_value = 601

            draw_grid(self.mock_screen)

            # Check if screen methods are called correctly
            self.mock_screen.tracer.assert_any_call(0)
            self.mock_screen.update.assert_called_once()
            self.mock_screen.tracer.assert_called_with(1)

            # Check if Turtle is created and configured correctly
            mock_turtle.assert_called_once()
            mock_turtle_instance = mock_turtle.return_value
            mock_turtle_instance.hideturtle.assert_called_once()

            # Check major line drawing
            mock_turtle_instance.pensize.assert_any_call(1)
            mock_turtle_instance.pencolor.assert_any_call("black")

            # Verify number of calls for major lines and scale
            self.assertEqual(mock_turtle_instance.penup.call_count, 28)
            self.assertEqual(mock_turtle_instance.pendown.call_count, 28)
            self.assertEqual(mock_turtle_instance.goto.call_count, 42)

            # Check scale drawing
            mock_turtle_instance.color.assert_called_with("black")
            mock_turtle_instance.write.assert_called()
            mock_turtle_instance.dot.assert_called_with(5)

            # Verify that the grid is centered correctly
            goto_calls = [call for call in mock_turtle_instance.method_calls if call[0] == 'goto']
            x_coords = [call[1][0] for call in goto_calls]
            y_coords = [call[1][1] for call in goto_calls]
            self.assertIn(400, x_coords)
            self.assertIn(-400, x_coords)
            self.assertIn(300, y_coords)
            self.assertIn(-300, y_coords)


if __name__ == '__main__':
    unittest.main()
