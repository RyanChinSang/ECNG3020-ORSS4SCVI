package org.tensorflow.demo;

import android.app.Service;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.AudioManager;
import android.media.ToneGenerator;
import android.os.IBinder;
import android.preference.PreferenceManager;
import android.speech.tts.TextToSpeech;
import android.speech.tts.TextToSpeech.OnInitListener;
import android.text.TextUtils;
import android.util.Log;
import android.widget.Toast;

import java.util.Locale;

public class ttsService extends Service implements OnInitListener {

    public static TextToSpeech tts;
    private String string;
    SharedPreferences sharedPreferences;

    @Override
    public IBinder onBind(Intent arg0) {
        return null;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        tts = new TextToSpeech(this, this);
        sharedPreferences =  PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
    }

    @Override
    public void onDestroy() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
        super.onDestroy();
    }

    @Override
    public void onStart(Intent intent, int startId) {
        super.onStart(intent, startId);
        string = intent.getStringExtra("key");
        if (!TextUtils.isEmpty(string)) {
            speak(string);
        } else {
            // Plays a tone for an empty string
            ToneGenerator toneG = new ToneGenerator(AudioManager.STREAM_MUSIC, 100);
            toneG.startTone(ToneGenerator.TONE_CDMA_DIAL_TONE_LITE, 100);
            Log.e("onStart.tts", "String is empty: " + string);
        }
    }

    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            int result = tts.setLanguage(Locale.UK);
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                Log.e("SpeakService", "Language is not available.");
            }
        } else if (status == TextToSpeech.ERROR) {
            Toast.makeText(getApplicationContext(), "Sorry! Text To Speech failed...", Toast.LENGTH_LONG).show();
        }
    }

    private void speak(String line) {
        if (line.equals("Text to Speech disabled")) {
            tts.speak(line, TextToSpeech.QUEUE_FLUSH, null);
        } else if (sharedPreferences.getBoolean("switch_set_tts", true)) {
            tts.speak(line, TextToSpeech.QUEUE_FLUSH, null);
        }
    }
}
