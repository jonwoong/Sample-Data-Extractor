# Web-Table-Scraper
HTML table scraping using ScraPy

# Dependencies
[ScraPy](https://scrapy.org/download/)
Tkinter

# Execution
`$ python scraper.py`

# Example
The following table comes from https://www.w3schools.com/html/html_tables.asp:
<table id="customers">
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
  <tr>
    <td>Ernst Handel</td>
    <td>Roland Mendel</td>
    <td>Austria</td>
  </tr>
  <tr>
    <td>Island Trading</td>
    <td>Helen Bennett</td>
    <td>UK</td>
  </tr>
  <tr>
    <td>Laughing Bacchus Winecellars</td>
    <td>Yoshi Tannamuri</td>
    <td>Canada</td>
  </tr>
  <tr>
    <td>Magazzini Alimentari Riuniti</td>
    <td>Giovanni Rovelli</td>
    <td>Italy</td>
  </tr>
</table>

In order to scrape this table, find a uniquely identifying attribute for this table and its value.

The tag for this table reads ```<table id="customers">```, so the field entries should look like

**URL:** https://www.w3schools.com/html/html_tables.asp

**Table Attribute:** id

**Attribtue Value:** customers

**Number of Columns:** 3
