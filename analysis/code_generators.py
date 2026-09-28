"""Map generator_verbatim in data/av_extraction.csv to the frozen lookup table.
Reads only identifiers, modality and generator columns (never outcome columns).
Writes data/generator_coding.csv and appends new generators to data/generator_lookup_additions.csv."""
import csv, datetime as dt
ROOT='.'
def dec(s):
    p=s.split('-')
    if len(p)==1: d=dt.date(int(p[0]),7,1)
    elif len(p)==2: d=dt.date(int(p[0]),int(p[1]),15)
    else: d=dt.date(*map(int,p))
    y=d.year; start=dt.date(y,1,1); n=(dt.date(y+1,1,1)-start).days
    return round(y+(d-start).days/n,3)

ADD=[ # generator, modality, family, architecture, date, basis, source, confidence
('GPT-SoVITS','audio','zero-shot cloning','few-shot VITS + GPT','2024-01-14','code release','GitHub RVC-Boss/GPT-SoVITS repository created 2024-01-14 (GitHub API)','high'),
('GPT-SoVITS v3','audio','zero-shot cloning','few-shot VITS + GPT','2025-02-28','code release','GitHub release 20250228v3 (GitHub API)','high'),
('StarGANv2-VC','audio','speech-to-speech conversion','GAN VC','2021-07-21','arXiv','arXiv 2107.10394 v1 (OpenAlex)','high'),
('PPG-VC','audio','speech-to-speech conversion','PPG-based VC','2021','paper','Liu et al. 2021, any-to-many VC with PPGs','low'),
('CosyVoice','audio','zero-shot cloning','LLM + flow matching','2024-07-07','arXiv','arXiv 2407.05407 v1 (OpenAlex)','high'),
('JETS','audio','parametric/early neural TTS','end-to-end TTS','2022-03-31','arXiv','arXiv 2203.16852 v1 (OpenAlex)','high'),
('MMS TTS (Fairseq)','audio','parametric/early neural TTS','VITS-based multilingual','2023-05-22','arXiv','arXiv 2305.13516 v1 (OpenAlex)','high'),
('Play.ht 2.0','audio','zero-shot cloning','commercial cloning','2023-09','product','Play.ht product announcement','low'),
('MLAAD (dataset)','audio','mixed (dataset)','dataset','2024-01','arXiv','arXiv 2401.09512 v1 (OpenAlex)','high'),
('ASVspoof 5 (dataset)','audio','mixed (dataset)','dataset','2024-08','arXiv','arXiv 2408.08739 v1 (OpenAlex)','high'),
('VoiceWukong (dataset)','audio','mixed (dataset)','dataset','2024-09','arXiv','arXiv 2409.06348 v1 (OpenAlex)','high'),
('AudioLDM','audio','general audio (exploratory)','latent diffusion','2023-01-29','arXiv','arXiv 2301.12503 v1 (OpenAlex)','high'),
('AudioLDM 2','audio','general audio (exploratory)','latent diffusion','2023-08-10','arXiv','arXiv 2308.05734 v1 (OpenAlex)','high'),
('DCASE 2023 Task 7 systems','audio','general audio (exploratory)','challenge submissions','2023-06','challenge','DCASE 2023 Task 7 results','low'),
('Suno v3','music','AI music (exploratory)','text-to-music','2024-03-21','product','Suno v3 announcement','medium'),
('Udio','music','AI music (exploratory)','text-to-music','2024-04-10','product','Udio public launch','medium'),
('Mureka','music','AI music (exploratory)','text-to-music','2025','product','Mureka launch','low'),
('SOUNDRAW','music','AI music (exploratory)','generative music service','2020','product','SOUNDRAW launch','low'),
('Veo 3.1','video','diffusion/transformer text-to-video','T2V','2025-10-15','product','TechCrunch 2025-10-15, "Google releases Veo 3.1, adds it to Flow video editor"','high'),
('Seedance 1.0 Pro','video','diffusion/transformer text-to-video','T2V','2025-06-10','arXiv','arXiv 2506.09113 v1 (OpenAlex)','high'),
('LTX-Video','video','diffusion/transformer text-to-video','T2V/I2V','2024-11-20','code release','GitHub Lightricks/LTX-Video created 2024-11-20 (GitHub API)','high'),
('Wan VACE','video','diffusion/transformer text-to-video','video editing','2025-03-10','arXiv','arXiv 2503.07598','medium'),
('Wan 2.2','video','diffusion/transformer text-to-video','T2V','2025-07-28','code release','GitHub Wan-Video/Wan2.2 created 2025-07-28 (GitHub API)','high'),
('Open-Sora 2.0','video','diffusion/transformer text-to-video','T2V','2025-03-12','arXiv','arXiv 2503.09642 v1 (OpenAlex)','high'),
('Allegro','video','diffusion/transformer text-to-video','T2V','2024-10-20','arXiv','arXiv 2410.15458 v1 (OpenAlex)','high'),
('RAVE (video editing)','video','diffusion/transformer text-to-video','diffusion video editing','2023-12-07','arXiv','arXiv 2312.04524 v1 (OpenAlex)','high'),
('InsightFace inswapper','video','face-swap autoencoder','face swap','2023-04-02','code release','insightface v0.7 release 2023-04-02 (GitHub API), which introduced the inswapper model','low'),
('Framer','video','diffusion/transformer text-to-video','interpolation','2024-10-24','arXiv','arXiv 2410.18978 v1 (OpenAlex)','high'),
('DiffuEraser','video','diffusion/transformer text-to-video','video inpainting','2025-01-17','arXiv','arXiv 2501.10018 v1 (OpenAlex)','high'),
('ProPainter','video','diffusion/transformer text-to-video','transformer video inpainting','2023-09-07','arXiv','arXiv 2309.03897 v1 (OpenAlex)','high'),
('FSGAN','video','face-swap autoencoder','GAN face swap','2019-08-16','arXiv','arXiv 1908.05932','medium'),
('Diff2Lip','video','GAN reenactment','diffusion lip sync','2023-08','arXiv','arXiv 2308.09716 v1 (OpenAlex)','high'),
('LatentSync','video','GAN reenactment','latent diffusion lip sync','2024-12-12','arXiv','arXiv 2412.09262 v1 (OpenAlex)','high'),
('TPSMM','video','GAN reenactment','motion transfer','2022-03-27','arXiv','arXiv 2203.14367 v1 (OpenAlex)','high'),
('HyperReenact','video','GAN reenactment','face reenactment','2023-07-20','arXiv','arXiv 2307.10797 v1 (OpenAlex)','high'),
('FADM','video','GAN reenactment','diffusion reenactment','2023-04-06','arXiv','arXiv 2304.03199 v1 (OpenAlex)','high'),
('AniFaceDiff','video','GAN reenactment','diffusion reenactment','2024-06-19','arXiv','arXiv 2406.13272 v1 (OpenAlex)','high'),
('FaceFusion','video','face-swap autoencoder','face swap tool','2023-08-17','code release','GitHub facefusion/facefusion created 2023-08-17 (GitHub API)','medium'),
('DFD (Google DeepFakeDetection, dataset)','video','mixed (dataset)','dataset','2019-09-24','blog','Google AI blog','medium'),
('DeepFake-TIMIT (dataset)','video','mixed (dataset)','dataset','2018-12-20','arXiv','arXiv 1812.08685 v1 (OpenAlex)','high'),
('UADFV (dataset)','video','mixed (dataset)','dataset','2018-06-07','arXiv','arXiv 1806.02877 v1 (OpenAlex)','high'),
('DF40 (dataset)','video','mixed (dataset)','dataset','2024-06-19','arXiv','arXiv 2406.13495 v1 (OpenAlex)','high'),
('AV-Deepfake1M (dataset)','audiovisual','mixed (dataset)','dataset','2023-11-26','arXiv','arXiv 2311.15308 v1 (OpenAlex)','high'),
('Trusted Media Challenge (dataset)','audiovisual','mixed (dataset)','dataset','2022-01-13','arXiv','arXiv 2201.04788 (month from arXiv ID; day not confirmed)','medium'),
('SyncTalk','video','GAN reenactment','NeRF talking head / lip sync','2023-11-29','arXiv','arXiv 2311.17590 v1 (OpenAlex)','high'),
('FoR Fake-or-Real (dataset)','audio','mixed (dataset)','dataset','2019-10','paper','Reimao & Tzerpos, SpeD 2019','medium'),
('MaskGCT','audio','zero-shot cloning','masked generative codec TTS','2024-09-01','arXiv','arXiv 2409.00750 v1','medium'),
('HierSpeech++','audio','zero-shot cloning','hierarchical VAE zero-shot TTS','2023-11-21','arXiv','arXiv 2311.12454 v1 (OpenAlex)','high'),
('Seed-VC','audio','speech-to-speech conversion','zero-shot diffusion VC','2024-11-15','arXiv','arXiv 2411.09943 v1 (OpenAlex)','high'),
('Wan 2.6','video','diffusion/transformer text-to-video','T2V (commercial)','2025-12','paper table','DF26 (arXiv 2609.07369) Table 1, release month','medium'),
('Grok Imagine 1.0','video','diffusion/transformer text-to-video','T2V (commercial)','2026-01','paper table','DF26 (arXiv 2609.07369) Table 1, release month','medium'),
('Kling 3.0','video','diffusion/transformer text-to-video','T2V (commercial)','2026-02','paper table','DF26 (arXiv 2609.07369) Table 1, release month','medium'),
('HunyuanVideo 1.5','video','diffusion/transformer text-to-video','T2V/I2V (open)','2025-11','paper table','DF26 (arXiv 2609.07369) Table 1, release month','medium'),
('LTX 2.3','video','diffusion/transformer text-to-video','T2V/I2V (open)','2026-03','paper table','DF26 (arXiv 2609.07369) Table 1, release month','medium'),
('Celeb-DF++ (dataset)','video','mixed (dataset)','dataset','2025-07','arXiv','Celeb-DF++ paper','low'),
('DeepSpeak v2 (dataset)','video','mixed (dataset)','dataset','2025','dataset','DeepSpeak v2 release','low'),
]
L={r['generator']:r for r in csv.DictReader(open('data/generator_lookup.csv'))}
A={a[0]:dict(generator=a[0],modality=a[1],family=a[2],release_decimal=dec(a[4])) for a in ADD}
ALL={**{k:dict(family=v['family'],release_decimal=float(v['release_decimal'])) for k,v in L.items()},**A}

EL='ElevenLabs Multilingual v2'
DFDC='DFDC (full dataset)'
P='pipeline dated by newest component'
# row_id prefix or exact -> (components list, status, note)
M={
'ST001':([DFDC],'coded',''),'ST004':([DFDC],'coded','hardest DFDC items (curation)'),'ST007':([DFDC],'coded',''),
'ST013':([DFDC],'coded',''),'ST018':([DFDC],'coded',''),'ST049':([DFDC],'coded',''),'ST061':([DFDC],'coded',''),
'ST027':(['DFDC preview (dataset)'],'coded',''),'ST047':(['DFDC preview (dataset)'],'coded',''),
'ST002':([EL],'coded','unversioned ElevenLabs IVC, rule 3'),'ST037':([EL],'coded','rule 3'),'ST062':([EL],'coded','rule 3'),
'ST074':([EL],'coded','rule 3'),'ST056':([EL],'coded',''),'ST071':([EL],'coded',''),'ST008':([EL],'coded','Voice Design rows coded to Multilingual v2 (low)'),
'ST003':(['VITS'],'coded',''),'ST025':(['YourTTS'],'coded',''),'ST029':(['SV2TTS (speaker-verification transfer TTS)'],'coded',''),
'ST017':(['HiFi-GAN'],'coded','Tacotron 2 + HiFi-GAN; '+P),'ST035':(['WaveGlow'],'coded','Tacotron 2 + WaveGlow; '+P),
'ST006':(['ASVspoof 2019 LA (dataset)'],'coded','attacks A07-A19'),
'ST005-a':(['Wav2Lip'],'coded','audio from voice actors (human)'),'ST005-b':(['Wav2Lip'],'coded','voice actor audio'),
'ST005-c':(['Wav2Lip'],'coded','voice actor audio'),'ST005-d':(['Wav2Lip'],'coded','voice actor audio'),'ST005-e':(['Wav2Lip'],'coded',''),
'ST005-f':(['Wav2Lip'],'coded','voice actor audio'),'ST005-g':(['Wav2Lip'],'coded','voice actor audio'),
'ST005-h':(['Wav2Lip','DeepFaceLab','ElevenLabs (beta platform)'],'coded','pooled components, rule 6; data 2023-06'),
'ST005-i':(['Wav2Lip','DeepFaceLab'],'coded','voice actor audio'),'ST005-j':(['FaceSwap (open-source)'],'coded','Agarwal 2019 face swaps; generic'),
'ST005-l':(['Wav2Lip','DeepFaceLab',EL],'coded','data 2023-12'),
'ST009-a':(['DeeperForensics-1.0 (dataset)'],'coded',''),'ST009-b':(['Celeb-DF (dataset)'],'coded',''),'ST009-c':([DFDC],'coded',''),
'ST009-d':(['DFD (Google DeepFakeDetection, dataset)'],'coded',''),'ST009-e':(['FaceForensics++ (dataset)'],'coded',''),
'ST009-f':(['DeepFake-TIMIT (dataset)'],'coded',''),'ST009-g':(['UADFV (dataset)'],'coded',''),
'ST010':([],'unresolved','commercial mix of tools, versions unknown; rule 8 class assignment pending'),
'ST011-a':(['DeepFaceLab'],'coded',''),'ST011-b':(['DeepFakes (original Reddit autoencoder)'],'coded','FF++ Deepfakes method'),
'ST011-c':(['Celeb-DF (dataset)'],'coded',''),'ST011-d':(['DeepFaceLab'],'coded',''),'ST011-e':(['DeepFakes (original Reddit autoencoder)'],'coded',''),
'ST011-f':(['DeepFaceLab'],'coded',''),'ST011-g':(['DeepFakes (original Reddit autoencoder)'],'coded',''),
'ST011-h':(['DeepFaceLab'],'coded',''),'ST011-i':(['DeepFakes (original Reddit autoencoder)'],'coded',''),
'ST015':(['Celeb-DF (dataset)'],'coded',''),'ST019':(['Celeb-DF (dataset)'],'coded',''),'ST113':(['Celeb-DF (dataset)'],'coded','Koebis 2021 stimuli'),
'ST021':(['DCASE 2023 Task 7 systems'],'exploratory','non-speech audio'),
'ST031':(['SV2TTS (speaker-verification transfer TTS)','Wav2Lip','FaceSwap (open-source)','FSGAN'],'coded','FakeAVCeleb constituents, rule 7'),
'ST033-a':(['ASVspoof 2021 (dataset)'],'coded',''),'ST033-b':(['WaveFake (dataset)'],'coded',''),
'ST033-c':(['SV2TTS (speaker-verification transfer TTS)'],'coded','FakeAVCeleb audio'),
'ST039-a':(['ASVspoof 2021 (dataset)'],'coded','LA+DF segments'),'ST039-b':([EL],'coded','ElevenLabs cloning 2023-24, rule 3'),
'ST042-a':(['Tortoise TTS'],'coded','partial fakes'),'ST042-b':(['Tortoise TTS','FreeVC'],'coded',''),
'ST044-a':([],'drop','pooled row; per-generator rows used (rule 5)'),'ST044-b':(['Sora (public)','Veo 2','Allegro'],'coded',''),
'ST044-c':(['Sora (public)','Veo 2','Allegro'],'coded',''),'ST044-d':(['Sora (public)','Veo 2','Allegro'],'coded',''),
'ST044-e':(['RAVE (video editing)'],'coded','partial manipulation'),'ST044-f':(['InsightFace inswapper'],'coded','partial'),
'ST044-g':(['Framer'],'coded','partial'),'ST044-h':(['DiffuEraser','ProPainter'],'coded','partial'),'ST044-i':([],'unresolved','AKiRA date unknown'),
'ST048':(['DeepFaceLab'],'coded','DeepTomCruise (Chris Ume); tool per press reports, low'),
'ST051':(['GPT-SoVITS v3'],'coded',''),'ST053':(['Celeb-DF (dataset)'],'coded','beautification filters (post-processing)'),
'ST055':(['VoiceWukong (dataset)'],'coded',''),'ST065':(['FreeVC','StarGANv2-VC','PPG-VC'],'coded','pooled, rule 6'),
'ST066-a':(['ASVspoof 2019 LA (dataset)','ASVspoof 2021 (dataset)'],'coded',''),'ST066-b':(['ASVspoof 2019 LA (dataset)'],'coded',''),
'ST066-c':(['ASVspoof 2021 (dataset)'],'coded',''),'ST066-d':(['ASVspoof 2019 LA (dataset)','ASVspoof 2021 (dataset)'],'coded',''),
'ST066-e':(['ASVspoof 2019 LA (dataset)'],'coded',''),'ST066-f':(['ASVspoof 2021 (dataset)'],'coded',''),
'ST066-g':(['ASVspoof 2019 LA (dataset)','ASVspoof 2021 (dataset)'],'coded',''),'ST066-h':(['ASVspoof 2019 LA (dataset)'],'coded',''),
'ST066-i':(['ASVspoof 2021 (dataset)'],'coded',''),
'ST072':([],'drop','40% non-generative spoofs, N=2 authors'),
'ST076-a':([],'drop','pooled row; per-generator rows used'),'ST076-b':(['Veo 3'],'coded',''),'ST076-c':(['LTX-Video'],'coded',''),'ST076-d':(['Wan VACE'],'coded',''),
'ST078':(['Play.ht 2.0'],'coded','withdrawn paper; unversioned product'),'ST081':(['Veo 3.1'],'coded',''),
'ST083':([],'excluded_rule8','generator not reported'),'ST087':([],'no_generator','community data; check'),
'ST090':([],'no_generator','check source'),'ST095':([],'no_generator','check source'),'ST114':([],'no_generator','check source'),
'ST092':(['Tortoise TTS'],'coded',''),'ST093':(['Suno v3','Udio','Mureka'],'exploratory','music'),
'ST096':(['XTTS v2 (Coqui)','MMS TTS (Fairseq)','OpenVoice','Diff2Lip','LatentSync'],'coded','GPT-TTS component undated, omitted'),
'ST098':(['JETS','YourTTS','XTTS v2 (Coqui)','GPT-SoVITS','CosyVoice','ElevenLabs v3'],'coded','localization task; ElevenLabs version per data date'),
'ST099-a':([],'unresolved','unnamed open-source aggregate'),'ST099-b':([],'unresolved','closed-source aggregate'),
'ST099-c':([],'unresolved','Seedance 2.0 date unknown'),'ST099-d':(['Kling'],'coded','version unresolved; coded to table row (low)'),
'ST100-a':(['FaceSwap (open-source)'],'coded','generic face swap, rule 8'),'ST100-b':(['DF40 (dataset)'],'coded',''),
'ST102':([],'unresolved','in-the-wild mix'),'ST103':(['Veo 3.1','Wan 2.2','Open-Sora 2.0','HunyuanVideo'],'coded',''),
'ST104-a':(['AudioLDM 2'],'exploratory','non-speech'),'ST104-b':(['AudioLDM 2'],'exploratory','non-speech'),'ST104-c':(['AudioLDM'],'exploratory','non-speech'),
'ST105-a':([],'drop','pooled row'),'ST105-b':(['AniFaceDiff'],'coded','implausible d-prime; verify'),'ST105-c':(['TPSMM'],'coded','verify'),
'ST105-d':([],'unresolved','FaceVid undated'),'ST105-e':(['HyperReenact'],'coded','verify'),'ST105-f':(['FaceFusion'],'coded','verify'),
'ST105-g':(['FADM'],'coded','verify'),'ST105-h':([],'drop','unnamed SOTA methods'),



'ST106-a':(['AV-Deepfake1M (dataset)'],'coded',''),'ST106-b':(['Trusted Media Challenge (dataset)'],'coded',''),
'ST091':([EL],'coded','ElevenLabs IVC Multilingual v2 (named)'),'ST144':([],'unresolved','in-the-wild deepfakes, tools not named'),
'ST139':(['Wan 2.2'],'coded',''),'ST126':([EL],'coded',''),'ST120':(['SV2TTS (speaker-verification transfer TTS)','Wav2Lip','FaceSwap (open-source)','FSGAN'],'coded','FakeAVCeleb constituents, rule 7'),
'ST077':([EL],'coded','ElevenLabs Voice Design, Dec 2024'),'ST060':([],'unresolved','political deepfakes, tool not named'),
'ST043':(['FaceForensics++ (dataset)',DFDC],'coded','pooled datasets'),'ST111':(['Suno v3','Udio'],'exploratory','music'),
'ST013':([DFDC],'coded',''),'ST028':(['FaceSwap (open-source)'],'coded','Agarwal 2019 face swaps and public deepfakes; generic (rule 8)'),
'ST082':(['Sora 2','Kling'],'coded','"AI models like Sora or Kling"; versions per data date (rule 3), Kling version unresolved'),
'ST108':(['Sora (public)'],'coded',''),'ST110':(['SOUNDRAW'],'exploratory','music'),
'ST115-a':(['MLAAD (dataset)','ASVspoof 5 (dataset)'],'coded','pooled over 138 systems; approximated by source datasets'),
'ST115-b':([],'unresolved','commercial family, products unnamed'),'ST115-c':(['VALL-E'],'coded','family label, earliest of class (rule 8)'),
'ST115-d':(['Tacotron'],'coded','family label, rule 8'),'ST115-e':(['Glow-TTS'],'coded','family label, rule 8'),'ST115-f':(['ASVspoof 5 (dataset)'],'coded',''),
'ST117':(['FaceFusion','SyncTalk','HierSpeech++','Seed-VC'],'coded','pooled over four manipulation families (rule 6); family tie resolved to newest'),
'ST140':(['DeepFaceLab'],'coded','real-time DeepFaceLab'),'ST119':(['MaskGCT'],'coded','MaskGCT zero-shot TTS (named in full text)'),
'ST124':(['DFD (Google DeepFakeDetection, dataset)'],'coded',''),'ST129':([],'excluded_rule8','tools not named'),
'ST131-a':(['SV2TTS (speaker-verification transfer TTS)'],'coded','RTVC'),'ST131-b':(['YourTTS'],'coded',''),
'ST131-c':([EL],'coded','ElevenLabs 2024'),
'ST133-a':(['Wan 2.6','Veo 3.1','Grok Imagine 1.0','Kling 3.0','Wan 2.2','HunyuanVideo 1.5','LTX 2.3'],'coded','DF26 generators from its Table 1; 3-option response'),'ST133-b':(['Celeb-DF++ (dataset)'],'coded',''),'ST133-c':(['DeepSpeak v2 (dataset)'],'coded',''),
'ST141-a':(['Seedance 1.0 Pro'],'coded',''),'ST141-b':(['Veo 3.1'],'coded',''),'ST141-c':(['Sora 2'],'coded',''),
'ST141-d':(['Veo 3.1','Seedance 1.0 Pro','Sora 2'],'coded',''),'ST141-e':(['Veo 3.1','Seedance 1.0 Pro','Sora 2'],'coded',''),
'ST145':([],'unresolved','BioDeepAV/DFW/DDL undated'),
'ST146':(['DeepFakes (original Reddit autoencoder)'],'coded','2018 Obama/Peele (FakeApp); voice human'),
'ST148':(['First Order Motion Model'],'coded',''),
'ST112':(['Wan 2.2'],'coded','named with version'),'ST132':([EL],'coded','ElevenLabs speech-to-speech, rule 3'),
'ST127':(['FoR Fake-or-Real (dataset)'],'coded','majority of stimuli from FoR; few commercial clones not separable'),
'ST125':([],'exploratory','ballot-video inpainting, not faces or voices'),'ST026':([],'drop','ineligible: still images'),
}
rows=[]
out=[]
for r in csv.DictReader(open('data/av_extraction.csv')):
    rid=r['row_id']; sid=r['study_id']
    if rid in M: comp,st,note=M[rid]
    elif sid in M: comp,st,note=M[sid]
    else: comp,st,note=[],'not_needed',''
    rel=fam=''
    if comp:
        for c in comp: assert c in ALL,c
        rel=round(sum(ALL[c]['release_decimal'] for c in comp)/len(comp),3)
        fams=[ALL[c]['family'] for c in comp]
        # rule 6: most common family, ties -> newest
        best=max(set(fams),key=lambda f:(fams.count(f),max(ALL[c]['release_decimal'] for c in comp if ALL[c]['family']==f)))
        fam=best
    out.append(dict(row_id=rid,study_id=sid,modality=r['modality'],generator_verbatim=r['generator_verbatim'],components=';'.join(comp),release_decimal=rel,family=fam,coding_status=st,coding_note=note))
fn=list(out[0].keys())
w=csv.DictWriter(open('data/generator_coding.csv','w',newline=''),fieldnames=fn);w.writeheader();w.writerows(out)
with open('data/generator_lookup_additions.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow('generator,modality,family,architecture,release_date,release_decimal,date_basis,source,confidence,added_on,reason'.split(','))
    for a in ADD: w.writerow([a[0],a[1],a[2],a[3],a[4],dec(a[4]),a[5],a[6],a[7],'2026-09-27','named in an included study; not in frozen table'])
import collections
print(collections.Counter(o['coding_status'] for o in out))
