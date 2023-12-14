import application.data.persistent_storage as pss


class Colour:
    @property
    def background(self):
        """
        Darkest

        :return: a colour
        """
        if pss.AppConfig.get_colour_theme("dark"):
            return "#363062"

    @property
    def medium(self):
        """
        Medium

        :return: a colour
        """
        if pss.AppConfig.get_colour_theme("dark"):
            return "#435585"

    @property
    def light(self):
        """
        Lightest

        :return: a colour
        """
        if pss.AppConfig.get_colour_theme("dark"):
            return "#818FB4"

    @property
    def foreground(self):
        """
        Foreground

        :return: a colour
        """
        if pss.AppConfig.get_colour_theme("dark"):
            return "#F5E8C7"

    @property
    def text(self):
        """
        Text

        :return: a colour
        """
        if pss.AppConfig.get_colour_theme("dark"):
            return "#000000"


COLOUR = Colour()
