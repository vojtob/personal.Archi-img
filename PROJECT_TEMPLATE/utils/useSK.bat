java -classpath xalan/xalan.jar;xalan/serializer.jar;xalan/xml-apis.jar;xalan/xercesImpl.jar org.apache.xalan.xslt.Process -IN ../Architecture_src/model/cpp.archimate -XSL xslt/useSK.xsl -OUT cpp.archimate
mv cpp.archimate ../Architecture_src/model