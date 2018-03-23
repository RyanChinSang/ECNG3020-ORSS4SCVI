package org.tensorflow.demo;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.TextView;

public class SetupOutroActivity extends AppCompatActivity {

    SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_outro);

        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        TextView textView = (TextView) findViewById(R.id.tv_outro_desc);
        String string = "All of your configurations have been successfully saved! @nl @nl";
        if (!sharedPreferences.getString("text_username", getString(R.string.pref_default_username)).equals(getString(R.string.pref_default_username))) {
            string = string + sharedPreferences.getString("text_username", getString(R.string.pref_default_username)) + ", you may now proceed to using our services.@nl @nl";
        }
        if (sharedPreferences.getString("list_set_stt", getString(R.string.pref_default_set_stt)).equals("2")) {
            string = string + "If you need my services, say 'ok assistant', and then ask me a question.";
        } else if (sharedPreferences.getString("list_set_stt", getString(R.string.pref_default_set_stt)).equals("1")) {
            string = string + "If you need my services, press the microphone button, and then ask me a question.";
        }
        string = string.replaceAll("@nl", System.getProperty("line.separator"));
        textView.setText(string);
    }

    public void gotoNext(View view) {
        Intent i = new Intent(SetupOutroActivity.this, DetectorActivity.class);
        i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(i);
    }

    public void gotoPrev(View view) {
        Intent i = new Intent(SetupOutroActivity.this, SetupPgFiveActivity.class);
        i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(i);
    }
}