<?xml version="1.0" encoding="UTF-8"?>
<!-- Presentación humana del sitemap.xml: los buscadores ignoran esta hoja
     de estilos y leen el XML crudo; los navegadores muestran esta tabla. -->
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html lang="es">
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title>Mapa del sitio — CASASILVIAWEB</title>
        <style>
          body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
                 margin: 0; padding: 24px 16px; background: #f6f6f7; color: #141417; }
          .wrap { max-width: 980px; margin: 0 auto; }
          h1 { font-size: 1.5rem; margin: 0 0 4px; }
          h1 span { color: #d21e28; }
          p.intro { color: #6b6b72; margin: 0 0 20px; font-size: .95rem; line-height: 1.5; }
          table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px;
                  overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,.06); font-size: .92rem; }
          th { background: #141417; color: #fff; text-align: left; padding: 10px 14px;
               font-size: .8rem; text-transform: uppercase; letter-spacing: .06em; }
          td { padding: 10px 14px; border-top: 1px solid #e6e6e9; word-break: break-word; }
          @media (max-width: 600px) { .prio, .num.date { display: none; } th.hprio, th.hdate { display: none; } }
          tr:nth-child(even) td { background: #fafafa; }
          a { color: #d21e28; text-decoration: none; font-weight: 600; }
          a:hover { text-decoration: underline; }
          .num { text-align: right; white-space: nowrap; color: #6b6b72; }
          .freq { white-space: nowrap; color: #6b6b72; }
        </style>
      </head>
      <body>
        <div class="wrap">
          <h1><span>CASASILVIAWEB</span> — Mapa del sitio</h1>
          <p class="intro">
            Este archivo (<b>sitemap.xml</b>) es para los buscadores: les dice qué páginas
            existen, cuándo se actualizaron ("lastmod"), cada cuánto suelen cambiar
            ("weekly" = semanalmente) y qué prioridad tiene cada una dentro del sitio.
            Total: <b><xsl:value-of select="count(s:urlset/s:url)"/> páginas</b>.
          </p>
          <table>
            <tr><th>Página</th><th class="hdate">Actualizada</th><th>Cambia</th><th class="hprio">Prioridad</th></tr>
            <xsl:for-each select="s:urlset/s:url">
              <tr>
                <td><a href="{s:loc}">/<xsl:value-of select="substring-after(s:loc, 'casasilviaweb.com.ar/')"/></a></td>
                <td class="num date"><xsl:value-of select="s:lastmod"/></td>
                <td class="freq"><xsl:value-of select="s:changefreq"/></td>
                <td class="num prio"><xsl:value-of select="s:priority"/></td>
              </tr>
            </xsl:for-each>
          </table>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
