import json
import couchdb
from dblogin import user, password
import sys

server = couchdb.Server("http://%s:%s@localhost:5984/" % (user, password))
dbname = "aurin"
if dbname in server:
    db = server[dbname]
else:
    db = server.create(dbname)

def read_population(file_path):
    with open(file_path, 'r') as f:
        line = f.read()
        # print(line)
        temp = json.loads(line)
        data = temp.get('features')
        for each_data in data:
            if each_data['properties']:
                output_data = {'type': 'population', 'city': each_data['properties']['sa4_name16'], \
                               'sa4_code16': each_data['properties']['sa4_code16'], \
                               'population': each_data['properties']['est_res_pop_ur_erp_30_jun_p_tot_num'], \
                               'population_desnity': each_data['properties']['pop_density_pop_density_p_p_km2']
                               }
                db.save(output_data)

def read_family(file_path):
    with open(file_path, 'r') as f:
        line = f.read()
        # print(line)
        temp = json.loads(line)
        data = temp.get('features')
        for each_data in data:
            if each_data['properties']:
                output_data = {'type': 'family', 'city': each_data['properties']['sa4_name16'], \
                               'sa4_code16': each_data['properties']['sa4_code16'], \
                               'access_internet': each_data['properties']['access_net_home_net_acsd_dwl_pr100'], \
                               'avg_commuting_from_home': each_data['properties']['commuting_wrk_avg_comdist_place_wrk_kms'], \
                               'family_num': each_data['properties']['fam_by_type_tot_fam_num'], \
                               'homeless_per_10000': each_data['properties']['homelessness_homelessness_rt10000_p_rt'], \
                               'total_employment': each_data['properties']['mtd_trvl_wrk_empy_p_tot_empy_num'], \
                               'avg_rent_payment_monthly': each_data['properties']['rent_mrtg_pay_avg_monthly_hsld_rent_payment_aud'], \
                               'avg_morgage_payment_monthly': each_data['properties']['rent_mrtg_pay_avg_monthly_hsld_mrtg_payment_aud']
                               }
                db.save(output_data)

def read_hospital(file_path):
    with open(file_path, 'r') as f:
        line = f.read()
        # print(line)
        temp = json.loads(line)
        data = temp.get('features')
        for each_data in data:
            if each_data['geometry']:
                coordinates = each_data['geometry']['coordinates']
            if each_data['properties']:
                output_data = {'type': 'hospital', 'coordinates': coordinates, \
                               'number_of_available_beds': each_data['properties']['number_of_available_beds'], \
                               }
                db.save(output_data)

def read_income(file_path):
    with open(file_path, 'r') as f:
        line = f.read()
        # print(line)
        temp = json.loads(line)
        data = temp.get('features')
        for each_data in data:
            if each_data['properties']:
                output_data = {'type': 'population', 'city': each_data['properties']['sa4_name16'], \
                               'sa4_code16': each_data['properties']['sa4_code_2016'], \
                               'mean_income_2011': each_data['properties']['mean_aud_2010_11'], \
                               'mean_income_2012': each_data['properties']['mean_aud_2011_12'], \
                               'mean_income_2013': each_data['properties']['mean_aud_2012_13'], \
                               'mean_income_2014': each_data['properties']['mean_aud_2013_14'], \
                               'mean_income_2015': each_data['properties']['mean_aud_2014_15']
                               }
                db.save(output_data)


read_population('population.json')
read_family('family.json')
read_hospital('hospital.json')
read_income('income.json')

db = server["aurin"]
with open("view_aurin.json") as file_object:
    db["_design/analysis"] = json.load(file_object)