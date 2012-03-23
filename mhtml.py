# HTML static content constants

header = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"\n \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n\
<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\">\n\
<head>\n\
    <link rel=\"stylesheet\" title=\"Standard\" href=\"styles.css\" type=\"text/css\" media=\"screen\" />\n\
    <script language=\"JavaScript\" type=\"text/javascript\" src=\"contentflow.js\" load=\"black\"></script>\n\
    <script tyle=\"text/javascript\">\n\
        var cf = new ContentFlow(\'contentFlow\', {reflectionColor: \"#000000\"});\n\
    </script>\n\
</head>\n"

body_start = "<body bgcolor=\"Black\">\n\
    <div class=\"maincontent\">\n\
    <!-- ===== Cover Flow ===== -->\n\
    <div id=\"contentFlow\" class=\"ContentFlow\">\n\
        <!-- should be place before flow so that contained images will be loaded first -->\n\
        <div class=\"loadIndicator\"><div class=\"indicator\"></div></div>\n\
        <div class=\"flow\">\n"
        
body_end = "\t</div>\n\
    <div class=\"globalCaption\"></div>\n\
    <div class=\"scrollbar\">\n\
        <div class=\"slider\"><div class=\"position\"></div></div>\n\
    </div>\n\
    </div>\n\
</body>\n\
</html>"