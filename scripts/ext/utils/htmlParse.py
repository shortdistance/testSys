#-*-coding:utf-8 -*-
import re

def filterHtmlTag(origHtml):
    """
    filter html tag, but retain its contents
    eg:
        Brooklyn, NY 11220<br />
        Brooklyn, NY 11220

        <a href="mailto:Bayridgenissan42@yahoo.com">Bayridgenissan42@yahoo.com</a><br />
        Bayridgenissan42@yahoo.com

        <a href="javascript:void(0);" onClick="window.open(new Array('http','',':','//','stores.ebay.com','/Bay-Ridge-Nissan-of-New-York?_rdc=1').join(''), '_blank')">stores.ebay.com</a>
        stores.ebay.com

        <a href="javascript:void(0);" onClick="window.open(new Array('http','',':','//','www.carfaxonline.com','/cfm/Display_Dealer_Report.cfm?partner=AXX_0&UID=C367031&vin=JH4KB2F61AC001005').join(''), '_blank')">www.carfaxonline.com</a>
        www.carfaxonline.com
    """
    #logging.info("html tag, origHtml=%s", origHtml);
    filteredHtml = origHtml;

    #Method 1: auto remove tag use re
    #remove br
    filteredHtml = re.sub("<br\s*>", "", filteredHtml, flags=re.I);
    filteredHtml = re.sub("<br\s*/>", "", filteredHtml, flags=re.I);
    #logging.info("remove br, filteredHtml=%s", filteredHtml);
    #remove a
    filteredHtml = re.sub("<a\s+[^<>]+>(?P<aContent>[^<>]+?)</a>", "\g<aContent>", filteredHtml, flags=re.I);
    #logging.info("remove a, filteredHtml=%s", filteredHtml);
    #remove b,strong
    filteredHtml = re.sub("<b>(?P<bContent>[^<>]+?)</b>", "\g<bContent>", filteredHtml, re.I);
    filteredHtml = re.sub("<strong>(?P<strongContent>[^<>]+?)</strong>", "\g<strongContent>", filteredHtml, flags=re.I);
    #logging.info("remove b,strong, filteredHtml=%s", filteredHtml);

    return filteredHtml;
