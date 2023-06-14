import unittest
from unittest.mock import MagicMock, Mock, mock_open, patch
import tkinter as tk
from Builder.Builder import Builder
from Builder.Director import Director
from Producer.BarGraph import BarGraph
from Producer.LineGraph import LineGraph
from Producer.PieGraph import PieGraph
from gui import App

class TestGui(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = App(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.filedialog.askopenfilename')
    def test_select_file(self, mock_askopenfilename):
        mock_askopenfilename.return_value = '/path/to/file'
        self.app.select_file()
        self.assertEqual(self.app.path, '/path/to/file')


    @patch('gui.Director')
    @patch('gui.BarGraph.BarGraph')
    def test_draw_chart_bar(self, mock_BarGraph, mock_Director):
        mock_builder = MagicMock()
        mock_BarGraph.return_value = mock_builder
        self.app.chart_type.set(1)
        self.app.draw_chart()
        mock_Director.assert_called_once()
        mock_director = mock_Director.return_value
        self.assertEqual(mock_director.builder, mock_builder)
        mock_director.build_graph.assert_called_once()

    @patch('gui.Director')
    @patch('gui.LineGraph.LineGraph')
    def test_draw_chart_line(self, mock_LineGraph, mock_Director):
        mock_builder = MagicMock()
        mock_LineGraph.return_value = mock_builder
        self.app.chart_type.set(2)
        self.app.draw_chart()
        mock_Director.assert_called_once()
        mock_director = mock_Director.return_value
        self.assertEqual(mock_director.builder, mock_builder)
        mock_director.build_graph.assert_called_once()

    @patch('gui.Director')
    @patch('gui.PieGraph.PieGraph')
    def test_draw_chart_pie(self, mock_PieGraph, mock_Director):
        mock_builder = MagicMock()
        mock_PieGraph.return_value = mock_builder
        self.app.chart_type.set(3)
        self.app.draw_chart()
        mock_Director.assert_called_once()
        mock_director = mock_Director.return_value
        self.assertEqual(mock_director.builder, mock_builder)
        mock_director.build_graph.assert_called_once()


    def test_update_draw_button_enabled(self):
        self.app.chart_type.set(1)
        self.app.update_draw_button()
        self.assertEqual(self.app.draw_button.cget("state"), "normal")

        self.app.chart_type.set(2)
        self.app.update_draw_button()
        self.assertEqual(self.app.draw_button.cget("state"), "normal")

        self.app.chart_type.set(3)
        self.app.update_draw_button()
        self.assertEqual(self.app.draw_button.cget("state"), "normal")

    def test_update_draw_button_disabled(self):
        self.app.chart_type.set(0)
        self.app.update_draw_button()
        self.assertEqual(self.app.draw_button.cget("state"), "disabled")

    @patch('tkinter.messagebox.askquestion')
    def test_close_yes(self, mock_askquestion):
        mock_askquestion.return_value = "yes"
        with patch.object(self.root, 'destroy') as mock_destroy:
            self.app.close()
            mock_destroy.assert_called_once()

    @patch('tkinter.messagebox.askquestion')
    def test_close_no(self, mock_askquestion):
        mock_askquestion.return_value = "no"
        with patch.object(self.root, 'destroy') as mock_destroy:
            self.app.close()
            mock_destroy.assert_not_called()

    def test_init(self):
        app = App(self.root)
        self.assertEqual(app.master, self.root)
        self.assertEqual(app.master.title(), "Rysuj wykres")
        self.assertEqual(app.master.geometry(), self.root.geometry())
        self.assertEqual(app.path, '')
        self.assertIsInstance(app.chart_type, tk.IntVar)


class TestDirector(unittest.TestCase):
    def test_build_graph(self):
        director = Director()
        builder = Mock()
        director.builder = builder
        director.build_graph()
        builder.open_file.assert_called_once()
        builder.prepare_chart.assert_called_once()
        builder.create_chart.assert_called_once()


class TestBuilder(unittest.TestCase):
    def test_builder(self):
        builder = Builder('path', True)
        self.assertEqual(builder.path, 'path')
        self.assertEqual(builder.content, '')
        self.assertEqual(builder.title, '')
        self.assertEqual(builder.is_title, True)

        builder.open_file = MagicMock()
        builder.prepare_chart = MagicMock()
        builder.create_chart = MagicMock()

        builder.open_file()
        builder.prepare_chart()
        builder.create_chart()

        builder.open_file.assert_called_once()
        builder.prepare_chart.assert_called_once()
        builder.create_chart.assert_called_once()


class TestLineGraph(unittest.TestCase):

    def setUp(self):
        self.line_graph = LineGraph("test.csv", True)

    def test_init(self):
        self.assertEqual(self.line_graph.path, "test.csv")
        self.assertEqual(self.line_graph.is_title, True)
        self.assertEqual(self.line_graph.x, [])
        self.assertEqual(self.line_graph.y, [])

    @patch("builtins.open", new_callable=mock_open, read_data="kolumna_x,kolumna_y\n1,4\n2,2\n3,3\n4,6\n5,5\n6,7")
    def test_open_file(self, mock_file):
        self.line_graph.open_file()
        self.assertEqual(self.line_graph.title, ["kolumna_x", "kolumna_y\n"])
        self.assertEqual(self.line_graph.x, [1, 2, 3, 4, 5, 6])
        self.assertEqual(self.line_graph.y, [4, 2, 3, 6, 5, 7])

    @patch("matplotlib.pyplot.xlabel")
    @patch("matplotlib.pyplot.ylabel")
    @patch("matplotlib.pyplot.title")
    def test_prepare_chart(self, mock_title, mock_ylabel, mock_xlabel):
        self.line_graph.title = ["kolumna_x", "kolumna_y"]
        self.line_graph.path = "test.csv"
        self.line_graph.prepare_chart()
        mock_xlabel.assert_called_with("kolumna_x")
        mock_ylabel.assert_called_with("kolumna_y")
        mock_title.assert_called_with("Wykres z pliku test.csv")

    @patch("matplotlib.pyplot.plot")
    @patch("matplotlib.pyplot.show")
    def test_create_chart(self, mock_show, mock_plot):
        self.line_graph.x = [1, 2]
        self.line_graph.y = [3, 4]
        self.line_graph.create_chart()
        mock_plot.assert_called_with([1, 2], [3, 4], color='#FF0000')
        mock_show.assert_called_once()


class TestBarGraph(unittest.TestCase):

    def setUp(self):
        self.bar_graph = BarGraph("test.csv", True)

    def test_init(self):
        self.assertEqual(self.bar_graph.path, "test.csv")
        self.assertEqual(self.bar_graph.is_title, True)
        self.assertEqual(self.bar_graph.x, [])
        self.assertEqual(self.bar_graph.y, [])

    @patch("builtins.open", new_callable=mock_open, read_data="kolumna_x,kolumna_y\n1,4\n2,2\n3,3\n4,6\n5,5\n6,7")
    def test_open_file(self, mock_file):
        self.bar_graph.open_file()
        self.assertEqual(self.bar_graph.title, ["kolumna_x", "kolumna_y\n"])
        self.assertEqual(self.bar_graph.x, [1, 2, 3, 4, 5, 6])
        self.assertEqual(self.bar_graph.y, [4, 2, 3, 6, 5, 7])

    @patch("matplotlib.pyplot.xlabel")
    @patch("matplotlib.pyplot.ylabel")
    @patch("matplotlib.pyplot.title")
    def test_prepare_chart(self, mock_title, mock_ylabel, mock_xlabel):
        self.bar_graph.title = ["kolumna_x", "kolumna_y"]
        self.bar_graph.path = "test.csv"
        self.bar_graph.prepare_chart()
        mock_xlabel.assert_called_with("kolumna_x")
        mock_ylabel.assert_called_with("kolumna_y")
        mock_title.assert_called_with("Wykres z pliku test.csv")

    @patch("matplotlib.pyplot.bar")
    @patch("matplotlib.pyplot.show")
    def test_create_chart(self, mock_show, mock_bar):
        self.bar_graph.x = [1, 2]
        self.bar_graph.y = [3, 4]
        self.bar_graph.create_chart()
        mock_bar.assert_called_with([1, 2], [3, 4], color='#32CD32')
        mock_show.assert_called_once()


class TestPieGraph(unittest.TestCase):

    def setUp(self):
        self.pie_graph = PieGraph("test.csv", True)

    def test_init(self):
        self.assertEqual(self.pie_graph.path, "test.csv")
        self.assertEqual(self.pie_graph.is_title, True)
        self.assertEqual(self.pie_graph.x, [])
        self.assertEqual(self.pie_graph.y, [])

    @patch("builtins.open", new_callable=mock_open, read_data="kolumna_x,kolumna_y\n1,4\n2,2\n3,3\n4,6\n5,5\n6,7")
    def test_open_file(self, mock_file):
        self.pie_graph.open_file()
        self.assertEqual(self.pie_graph.title, ["kolumna_x", "kolumna_y\n"])
        self.assertEqual(self.pie_graph.x, [1, 2, 3, 4, 5, 6])
        self.assertEqual(self.pie_graph.y, [4, 2, 3, 6, 5, 7])

    @patch("matplotlib.pyplot.title")
    def test_prepare_chart(self, mock_title):
        self.pie_graph.path = "test.csv"
        self.pie_graph.prepare_chart()
        mock_title.assert_called_with("Wykres z pliku test.csv")

    @patch("matplotlib.pyplot.pie")
    @patch("matplotlib.pyplot.show")
    def test_create_chart(self, mock_show, mock_pie):
        self.pie_graph.x = [1, 2]
        self.pie_graph.y = [3, 4]
        self.pie_graph.create_chart()
        mock_pie.assert_called_with([3, 4], labels=[1, 2])
        mock_show.assert_called_once()


if __name__ == '__main__':
    unittest.main()
