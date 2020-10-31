<?xml version="1.0" encoding="utf-8"?>
<s:stylesheet xmlns:s="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <s:output method="html" encoding="utf-8" omit-xml-declaration="yes" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" media-type="text/html" indent="no"/>
  <s:strip-space elements="*"/>
  <s:param name="current-time"/>
  <!-- -->
  <s:template match="/ScapiRequest/*">
    <tr>
      <td>
        <time>
          <s:value-of select="$current-time"/>
        </time>
      </td>
      <td>
        <code>
          <s:value-of select="name(.)"/>
        </code>
      </td>
      <td>
        <s:apply-templates/>
      </td>
    </tr>
  </s:template>
  <!-- -->
  <s:template match="output">
    <ul>
      <s:apply-templates/>
    </ul>
  </s:template>
  <!-- -->
  <s:template match="print/type/*">
    <s:value-of select="name(.)"/>
  </s:template>
  <!-- -->
  <s:template match="ssn | msg | nokReason | selectedService">
    <li>
      <s:value-of select="concat(name(.), ':', name(./*[1]))"/>
    </li>
  </s:template>
  <!-- -->
  <s:template match="interfaceStatus">
    <ul class="update_interface">
      <s:call-template name="interface-status">
        <s:with-param name="name">Chip reader</s:with-param>
        <s:with-param name="bit" select="1"/>
      </s:call-template>
      <s:call-template name="interface-status">
        <s:with-param name="name">Magnetic stripe reader</s:with-param>
        <s:with-param name="bit" select="2"/>
      </s:call-template>
      <s:call-template name="interface-status">
        <s:with-param name="name">Attendant numeric keypad</s:with-param>
        <s:with-param name="bit" select="3"/>
      </s:call-template>
      <s:call-template name="interface-status">
        <s:with-param name="name">Attendant F key manual entry</s:with-param>
        <s:with-param name="bit" select="4"/>
      </s:call-template>
      <s:call-template name="interface-status">
        <s:with-param name="name">Attendant F key reference entry</s:with-param>
        <s:with-param name="bit" select="5"/>
      </s:call-template>
      <s:call-template name="interface-status">
        <s:with-param name="name">Attendant F key accept</s:with-param>
        <s:with-param name="bit" select="6"/>
      </s:call-template>
      <s:call-template name="interface-status">
        <s:with-param name="name">Attendant contactless reader</s:with-param>
        <s:with-param name="bit" select="7"/>
      </s:call-template>
      <s:call-template name="interface-status">
        <s:with-param name="name">Cardholder detection</s:with-param>
        <s:with-param name="bit" select="8"/>
      </s:call-template>
    </ul>
  </s:template>
  <!-- -->
  <s:template name="interface-status">
    <s:param name="bit"/>
    <s:param name="name"/>
    <li>
      <abbr>
        <s:attribute name="title">
          <s:value-of select="$name"/>
        </s:attribute>
        <s:value-of select="substring(.,$bit,1)"/>
      </abbr>
    </li>
  </s:template>
</s:stylesheet>
