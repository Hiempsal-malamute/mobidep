import pandas as pd 
import geopandas as gpd 
import dask.dataframe as dd

migdep_init = dd.read_csv("FD_MIGGCO_2019.csv",sep=";",dtype={"COMMUNE":str,"IPONDI":float,"DRAN":str})

# besoin des colonnes : DEPT, IPONDI, IRAN
migdep = migdep_init[["COMMUNE","DRAN","IPONDI"]]

# création colonne DACT : "département de résidence actuel"
migdep["DRACT"] = migdep["COMMUNE"].str.slice(0,2)
migdep = migdep[["DRACT","DRAN","IPONDI"]]

# agrégation et comptage du nb de ménages ayant déménagé par departement de résidence actuel
count = migdep.groupby(["DRAN","DRACT"]).count().reset_index().compute()

# conversion code dep en caractère
count = count.astype({"DRAN":"string","IPONDI":"float"})
count.dtypes

count.to_csv("total_migrations.csv",index=False)