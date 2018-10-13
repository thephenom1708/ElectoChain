/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package fusioncharts;

public class FusionCharts {
	private String constructorTemplate = "<script type=\"text/javascript\">\nFusionCharts.ready(function () {\n\tvar fc_chart = new FusionCharts(%s);\n%sfc_chart.render();\n});\n</script>";
	private String eventTemplate = "    fc_chart.addEventListener(\"%s\",%s);\n";
	private String messageTemplate = ",%s:\"%s\"";
	private String[] chartOptions = new String[10];
    private String chartDataSource = "";
    private String fusionChartsEvents = "";
    private String fusionChartsMessages = "";
    
    public FusionCharts(String type, String id, String width, String height, String renderAt, String dataFormat, String dataSource) {
        this.chartOptions[0] = id;
        this.chartOptions[1] = width;
        this.chartOptions[2] = height;
        this.chartOptions[3] = renderAt;
        this.chartOptions[4] = type;
        this.chartOptions[5] = dataFormat;
        //this.chartOptions[6] = "%s"; 
        if(this.chartOptions[5].contains("url")) {
            this.chartOptions[7] = "\""+dataSource+"\"";
        } else {
        	this.chartOptions[7] = "%s";
            this.chartDataSource = this.addSlashes(dataSource.replaceAll("\n", ""));
        }
        
    }
    
    private String addSlashes(String str) {
        str = str.replaceAll("\\\\", "\\\\\\\\");
        str = str.replaceAll("\\n", "\\\\n");
        str = str.replaceAll("\\r", "\\\\r");
        str = str.replaceAll("\\00", "\\\\0");
        str = str.replaceAll("u003d", "=");
        str = str.replaceAll("'", "\\\\'");
        str = str.replaceAll("\\\\", "");
        str = str.replaceAll("\"\\{", "{");
        str = str.replaceAll("\"\\[", "[");
        str = str.replaceAll("\\}\\]\"", "}]");
        str = str.replaceAll("\"\\}\"", "\"}");
        str = str.replaceAll("\\}\"\\}", "}}");
        return str;
    }
    
    private String jsonEncode(String[] data){
        String json = "{type: \""+this.chartOptions[4]+"\",renderAt: \""+this.chartOptions[3]+"\",width: \""+this.chartOptions[1]+"\",height: \""+this.chartOptions[2]+"\",dataFormat: \""+this.chartOptions[5] + "\"," + 
        				"id:\"" + this.chartOptions[0] + "\"" + this.fusionChartsMessages + ",dataSource: "+this.chartOptions[7]+"}";
        return json;
    }
    
    public String render() {
        String outputHTML;
        if(this.chartOptions[5].contains("url")) {
            outputHTML = String.format(this.constructorTemplate, this.jsonEncode(this.chartOptions));
            
        } else {
            if("json".equals(this.chartOptions[5])) {
            	this.chartOptions[7] = String.format(this.chartOptions[7], this.chartDataSource);
            	outputHTML = String.format(this.constructorTemplate, this.jsonEncode(this.chartOptions), fusionChartsEvents);
            } else {
            	this.chartOptions[7] = String.format(this.chartOptions[7], "\'"+ this.chartDataSource + "\'");
            	outputHTML = String.format(this.constructorTemplate, this.jsonEncode(this.chartOptions), fusionChartsEvents);
            }
        }
        return outputHTML;
    }
    
    public void addEvent(String eventName, String funcName){
    	String eventHTML;
    	eventHTML = String.format(this.eventTemplate, eventName, funcName);
    	this.fusionChartsEvents += eventHTML;
    }
    
    public void addMessage(String messageName, String messageText){
    	String messageString;
    	messageString = String.format(this.messageTemplate, messageName, messageText);
    	this.fusionChartsMessages += messageString;
    }
}
