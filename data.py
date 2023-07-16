import pandas as pd 
import geopandas as gpd 
import dask.dataframe as dd

migdep_init = dd.read_csv("data/raw/FD_MIGGCO_2019.csv",sep=";",dtype={"COMMUNE":str,"IPONDI":float,"DRAN":str})
ctr_dep = gpd.read_file("data/raw/fr-drom_ctr_dep2020_2154_style-1_gen.gpkg")[["insee_dep","geometry"]]

ctr_dep["geometry"] = ctr_dep.geometry.to_crs(4326)
ctr_dep["lat"] = ctr_dep["geometry"].y
ctr_dep["lng"] = ctr_dep["geometry"].x

ctr_dep = ctr_dep[["insee_dep","lat","lng"]]

# besoin des colonnes : DEPT, IPONDI, IRAN
migdep = migdep_init[["COMMUNE","DRAN","IPONDI"]]

# création colonne DACT : "département de résidence actuel"
migdep["DRACT"] = migdep["COMMUNE"].str.slice(0,2)
migdep = migdep[["DRACT","DRAN","IPONDI"]]

# agrégation et comptage du nb de ménages ayant déménagé par departement de résidence actuel
count_init = migdep.groupby(["DRAN","DRACT"]).count().reset_index().compute()

# conversion code dep en caractère
count = count_init.astype({"DRAN":"string","DRACT":"string","IPONDI":"float"})
count["DRAN"] = count["DRAN"].str.strip()
count.dtypes
count

ctr_dract = ctr_dep.rename(columns={"lat":"lat_dest","lng":"lng_dest"})
ctr_dran = ctr_dep.rename(columns={"lat":"lat_src","lng":"lng_src"})
ctr_dran.columns

new = count.merge(ctr_dract,"left",left_on="DRACT",right_on="insee_dep")
new1 = new.merge(ctr_dran,"left",left_on="DRAN",right_on="insee_dep")

# filtre pour supprimer les mobilités internes
new1 = new1[new1["DRACT"] != new1["DRAN"]]
new1

new1.to_csv("data/mig-res-2019.csv",index=False)