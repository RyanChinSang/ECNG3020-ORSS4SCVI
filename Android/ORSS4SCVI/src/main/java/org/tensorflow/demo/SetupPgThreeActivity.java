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

public class SetupPgThreeActivity extends AppCompatActivity {

    SharedPreferences sharedPreferences;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_pg_three);

        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        Switch set_confstr = (Switch) findViewById(R.id.switch_set_confstr);
        set_confstr.setChecked(sharedPreferences.getBoolean("switch_set_confstr", Boolean.valueOf(getString(R.string.pref_default_set_confstr))));
    }

    public void gotoNext(View view) {
        setPrefs();

        Intent i = new Intent(SetupPgThreeActivity.this, SetupPgFourActivity.class);
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
                        Intent i = new Intent(SetupPgThreeActivity.this, DetectorActivity.class);
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

        Intent i = new Intent(SetupPgThreeActivity.this, SetupPgTwoActivity.class);
        i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(i);
    }

    public void setPrefs() {
        Switch set_confstr = (Switch) findViewById(R.id.switch_set_confstr);
        Boolean switch_set_confstr = set_confstr.isChecked();
        sharedPreferences.edit().putBoolean("switch_set_confstr", switch_set_confstr).apply();
    }
}