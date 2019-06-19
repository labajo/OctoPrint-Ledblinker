# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import RPi.GPIO as GPIO
from .utils.PerpetualAlternatedTimer import PerpetualAlternatedTimer


class LedblinkerPlugin(octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.StartupPlugin):
    ##~~ StartupPlugin mixin

    def on_startup(self, *args, **kwargs):
        self._logger.info("GPIOBlinker starting up")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.get_settings_defaults()['led_pin'], GPIO.OUT, initial=GPIO.HIGH)

    def on_after_startup(self):
        self._logger.info("GPIOBlinker started up")
        t = PerpetualAlternatedTimer(self.get_settings_defaults()['off_delay'],
                                     self.get_settings_defaults()['on_delay'],
                                     self.led_off,
                                     self.led_on
                                     )
        t.start()

    def led_off(self):
        # self._logger.info("Thread")
        GPIO.output(self.get_settings_defaults()['led_pin'], GPIO.LOW)

    def led_on(self):
        # self._logger.info("Thread2")
        GPIO.output(self.get_settings_defaults()['led_pin'], GPIO.HIGH)

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            {
                'led_pin': 16,
                'off_delay': 10,
                'on_delay': 1
            }
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/ledblinker.js"],
            css=["css/ledblinker.css"],
            less=["less/ledblinker.less"]
        )

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            ledblinker=dict(
                displayName="Ledblinker Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="labajo",
                repo="OctoPrint-Ledblinker",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/labajo/OctoPrint-Ledblinker/archive/{target_version}.zip"
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Ledblinker Plugin"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = LedblinkerPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
