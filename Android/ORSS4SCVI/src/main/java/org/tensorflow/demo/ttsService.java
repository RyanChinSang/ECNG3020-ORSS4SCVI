/*
*
* */

package org.tensorflow.demo;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.speech.tts.TextToSpeech;
import android.speech.tts.TextToSpeech.OnInitListener;
import android.text.TextUtils;
import android.util.Log;
import android.widget.Toast;

import java.util.Locale;

public class ttsService extends Service implements OnInitListener {

    public static TextToSpeech tts;
    private String string;

    @Override
    public IBinder onBind(Intent arg0) {
        return null;
    }

    @Override
    public void onCreate() {
        tts = new TextToSpeech(this, this);
        super.onCreate();
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
            // TODO (feature [MED]): Play an error tone here?
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
        tts.speak(line, TextToSpeech.QUEUE_FLUSH, null);
    }
}
