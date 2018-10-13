from django.http import HttpResponse
import json
from collections import OrderedDict

# Common base class for FC
class FusionCharts:

    baseTemplate = """
        <script type="text/javascript">
            FusionCharts.ready(function () {
                __FC__
            });
        </script>"""

    constructorTemplate = """new FusionCharts(__constructorOptions__);"""
    renderTemplate = """FusionCharts("__chartId__").render();"""
    eventTemplate = """FusionCharts("__chartId__").addEventListener("_fceventname_",_fceventbody_);"""
    

    # constructor
    def __init__(self, type, id, width, height, renderAt, dataFormat, dataSource): 
        self.eventOptions = OrderedDict()
        self.constructorOptions = {}  
        self.constructorOptions['type'] = type
        self.constructorOptions['id'] = id
        self.constructorOptions['width'] = width
        self.constructorOptions['height'] = height
        self.constructorOptions['renderAt'] = renderAt
        self.constructorOptions['dataFormat'] = dataFormat
        #dataSource = unicode(dataSource, errors='replace')
        self.constructorOptions['dataSource'] = dataSource

    def addEvent(self, eventName, funcName):
        self.eventOptions[eventName] = funcName

    def addMessage(self, messageName, messageValue):
        self.constructorOptions[messageName] = messageValue

    # render the chart created
    # It prints a script and calls the FusionCharts javascript render method of created chart   
    def render(self):
        
        # Serialize constructorOptions to a JSON formatted
        self.readyJson = json.dumps(self.constructorOptions, ensure_ascii=False)

        # Create Fusioncharts constructor from template and insert JSON data in it
        self.readyJson = FusionCharts.constructorTemplate.replace('__constructorOptions__', self.readyJson)

        # Iterate and attach EventHandler from template
        for key, value in self.eventOptions.items():
            self.readyJson = self.readyJson + FusionCharts.eventTemplate.replace('__chartId__', self.constructorOptions['id'])
            self.readyJson = self.readyJson.replace("_fceventname_", key).replace("_fceventbody_", value)

        # FusionCharts Render method will create chart
        self.readyJson = self.readyJson + FusionCharts.renderTemplate.replace('__chartId__', self.constructorOptions['id'])
        self.readyJson = FusionCharts.baseTemplate.replace("__FC__", self.readyJson)

        self.readyJson = self.readyJson.replace('\\n', '')
        self.readyJson = self.readyJson.replace('\\t', '')

        if(self.constructorOptions['dataFormat'] == 'json'):
            self.readyJson = self.readyJson.replace('\\', '')
            self.readyJson = self.readyJson.replace('"{', "{")
            self.readyJson = self.readyJson.replace('}"', "}")

        return self.readyJson