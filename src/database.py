import sqlite3
con = sqlite3.connect("GenePanelRepo.db")

cur = con.cursor()

#cur.execute('CREATE TABLE GenePanelTable(unique_ID, version, disease, genes_in_panel, version_created)')

#res = cur.execute('SELECT unique_ID FROM GenePanelTable')
#res.fetchone()

cur.execute("INSERT INTO GenePanelTable VALUES(1, 1.1, 'Stickler syndrome', 'BMP4', '2023-10-26')")
con.commit()

res = cur.execute('SELECT unique_ID FROM GenePanelTable')
print(res.fetchone())


