package org.tensorflow.demo;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Switch;

public class SetupPgFiveActivity extends AppCompatActivity {

    SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_pg_five);

        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        Switch set_tts = (Switch) findViewById(R.id.switch_set_tts);
        set_tts.setChecked(sharedPreferences.getBoolean("switch_set_tts", Boolean.valueOf(getString(R.string.pref_default_set_tts))));
    }

    public void gotoNext(View view) {
        //gotoNext
        setPrefs();

        Intent i = new Intent(SetupPgFiveActivity.this, SetupOutroActivity.class);
        i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(i);
    }

    public void gotoSkip(View view) {
        AlertDialog alertDialog = new AlertDialog.Builder(this).create();
        alertDialog.setTitle(getString(R.string.setup_skip_title));
        alertDialog.setMessage(getString(R.string.setup_skip_message));
        alertDialog.setButton(AlertDialog.BUTTON_POSITIVE, "OK",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        Intent i = new Intent(SetupPgFiveActivity.this, DetectorActivity.class);
                        i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);
                        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        startActivity(i);
                    }
                });
        alertDialog.setButton(AlertDialog.BUTTON_NEGATIVE, "Cancel",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });
        alertDialog.show();
    }

    public void gotoPrev(View view) {
        //gotoPrev
        setPrefs();

        Intent i = new Intent(SetupPgFiveActivity.this, SetupPgFourActivity.class);
        i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(i);
    }

    public void setPrefs() {
        Switch set_tts = (Switch) findViewById(R.id.switch_set_tts);
        Boolean switch_set_tts = set_tts.isChecked();
        sharedPreferences.edit().putBoolean("switch_set_tts", switch_set_tts).apply();
    }
}