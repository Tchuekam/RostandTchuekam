# External Drive Migration — 28 May 2026

## Situation
C: drive at 99% (1.7 GB free of 106 GB). H: drive available with 63 GB free.

## What Was Moved to H:\CLINIC_BACKUP\

| Folder on C: | Moved To (H:) | Status |
|---|---|---|
| Desktop\01-DOCUMENTS | CLINIC_BACKUP\01-DOCUMENTS | ✅ |
| Desktop\02-PROJECTS-TCHUEKAM | CLINIC_BACKUP\PROJECTS-TCHUEKAM | ✅ |
| Desktop\03-MARKETING-COM | CLINIC_BACKUP\MARKETING-COM | ✅ |
| Desktop\04-SCRIPTS-CODE | CLINIC_BACKUP\SCRIPTS-CODE | ✅ |
| Desktop\05-BUSINESS-CLIENTS | CLINIC_BACKUP\BUSINESS-CLIENTS | ✅ |
| Desktop\07-DOWNLOADS-ARCHIVES | CLINIC_BACKUP\DOWNLOADS-ARCHIVES | ✅ |
| Desktop\08-WEB-RESEARCH | CLINIC_BACKUP\WEB-RESEARCH | ✅ |
| Desktop\MYFOLDER (partial) | CLINIC_BACKUP\MYFOLDER | ⏳ WEBAPPS conflict with H:\WEBAPPS |
| Desktop\cliente | CLINIC_BACKUP\cliente | ✅ |
| Desktop\TCHUEKAM_DAILY_REPORT | CLINIC_BACKUP\TCHUEKAM_DAILY_REPORT | ✅ |
| TCHUEKAM_QUAD_AGENT_SYSTEM | CLINIC_BACKUP\TCHUEKAM_QUAD | ✅ |
| Pictures | CLINIC_BACKUP\Pictures | ✅ |
| Music | CLINIC_BACKUP\Music | ✅ |
| Videos | CLINIC_BACKUP\Videos | ⏳ Timed out (large files) |
| node_modules | CLINIC_BACKUP\node_modules | ⏳ Timed out (many small files) |
| Downloads\Antigravity_IDE.exe | — | ❌ Locked/running |

## User Exclusions (Left Intact on C:\Desktop)
- LuckyTechHub-Bot-main
- 06-RACCOURCIS (shortcuts)
- HOMEAPPS (app shortcuts)
- wacrm (WhatsApp CRM)
- YOUTUBE_EMPIRE

## Pitfalls Encountered
1. **Inter-device mv is slow**: C: and H: are separate physical drives. `mv` copies then deletes — ~2× slower than on same drive.
2. **Directory name collision**: H: already had `WEBAPPS/` folder. `mv WEBAPPS` to H: failed with "Directory not empty". Solution: rename source to `WEBAPPS_DESKTOP`.
3. **Locked .exe file**: `Antigravity_IDE.exe` in Downloads was likely still in a running/pending state. Could not move.
4. **Terminal saturation**: Running multiple heavy `mv` commands concurrently caused git-bash terminal to hang/timeout on basic commands like `pwd`. Solution: move one folder at a time, wait for each to complete.
5. **du -sh timeouts at 99% disk**: Standard disk usage commands cannot finish before timeout on a choked disk. Use `ls | wc -l` as a lightweight probe instead.

## Commands Used
```bash
# Create destination hierarchy
mkdir -p /h/CLINIC_BACKUP/{DOCUMENTS,PROJECTS-TCHUEKAM,...}

# Move folder to H:
mv /c/Users/CLINIC/Desktop/01-DOCUMENTS /h/CLINIC_BACKUP/01-DOCUMENTS/

# Handle name collision
mv /c/Users/CLINIC/Desktop/MYFOLDER/WEBAPPS /h/CLINIC_BACKUP/MYFOLDER/WEBAPPS_DESKTOP

# Check what remains
ls /c/Users/CLINIC/
```
