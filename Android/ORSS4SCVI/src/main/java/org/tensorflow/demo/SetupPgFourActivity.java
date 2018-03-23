package org.tensorflow.demo;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.RadioGroup;

public class SetupPgFourActivity extends AppCompatActivity {

    SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_pg_four);

        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        RadioGroup set_stt = (RadioGroup) findViewById(R.id.list_set_stt);
        if (!sharedPreferences.getString("list_set_stt", getString(R.string.pref_default_set_stt)).equals(getString(R.string.pref_default_set_stt))) {
            set_stt.clearCheck();
            set_stt.check(sharedPreferences.getInt("list_set_stt_setup", R.string.pref_default_set_stt));
        }
    }

    public void gotoNext(View view) {
        setPrefs();

        Intent i = new Intent(SetupPgFourActivity.this, SetupPgFiveActivity.class);
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
                        Intent i = new Intent(SetupPgFourActivity.this, DetectorActivity.class);
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
        setPrefs();

        Intent i = new Intent(SetupPgFourActivity.this, SetupPgThreeActivity.class);
        i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(i);
    }

    public void setPrefs() {
        RadioGroup set_stt = (RadioGroup) findViewById(R.id.list_set_stt);
        sharedPreferences.edit().putString("list_set_stt", getString(Integer.parseInt(String.valueOf(set_stt.getCheckedRadioButtonId())))).apply();
        sharedPreferences.edit().putInt("list_set_stt_setup", Integer.parseInt(String.valueOf(set_stt.getCheckedRadioButtonId()))).apply();
    }
}