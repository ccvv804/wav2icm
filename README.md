# wav2icm
wav to hana ICM audio encoder
<pre><code>pip install wavio
python wav2icm2.py sample.wav
</code></pre>
PCM wav 오디오를 hana ICM로 변환해주는 인코더 입니다. 

## 정보
11025/22050/44100Hz mono/stereo PCM wav만 지원합니다.

알고리즘 문제로 임시로 사용하는 aiff 파일이 남아 있게 됩니다. 이것은 수동으로 삭제하시면 됩니다.

sample.wav는 Mike Koenig가 [soundbible](https://soundbible.com/1003-Ta-Da.html)으로 업로드한 wav파일입니다.
