import requests, time

API='http://127.0.0.1:8000'

# Simple surge: increase occupancy for Z1, Z2, Z3
for occ in [500, 1500, 3000, 4200]:
    payload={"zone_updates":[{"zone_id":"Z1","occupancy":occ},{"zone_id":"Z2","occupancy":int(occ*0.8)},{"zone_id":"Z3","occupancy":int(occ*0.6)}]}
    r=requests.post(API+"/ingest/heatmap", json=payload)
    print(r.status_code, r.text)
    time.sleep(2)

print('Done')
