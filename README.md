# spoke
This application only run on physical devices only. Device must configured by sound speaker.

**Run without docker**
```
source env/bin/activate
python index.py
```

**Run with docker**
```
docker compose up --build -d
docker compose ps
```

**API list**
1. Test connection
   ```
   curl http://192.168.0.121:3000
   ```
2. Play sound on resources file
   ```
   curl http://192.168.0.121:3000/play?file=./resources/speech.mp3
   ```
3. Speech from text
   ```
   curl http://192.168.0.121:3000/speech?text=Hello_World&lan=en
   ```
4. speech from text with auto detect language
   ```
   curl http://192.168.0.121:3000/speech?text=Perhatian
   ```
5. Speech from text to another language
   ```
   curl http://192.168.0.121:3000/t_lan?text=selamat_malam&frm_lan=ms&to_lan=en
   ```
6. Get status player
   ```
   curl http://192.168.0.121:3000/status
   ```
7. Stop player
   ```
   curl http://192.168.0.121:3000/stop
   ```
   
