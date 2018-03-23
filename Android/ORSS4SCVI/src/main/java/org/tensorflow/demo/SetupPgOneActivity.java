// TODO: ADD BSOP
package org.tensorflow.demo;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.Switch;

public class SetupPgOneActivity extends AppCompatActivity {

    SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_pg_one);

        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        if (!sharedPreferences.getString("text_username", getString(R.string.pref_default_username)).equals(getString(R.string.pref_default_username))) {
            EditText username = (EditText) findViewById(R.id.text_username);
            username.setText(sharedPreferences.getString("text_username", getString(R.string.pref_default_username)));
        }

        Switch bscreen = (Switch) findViewById(R.id.switch_bscreen);
        bscreen.setChecked(sharedPreferences.getBoolean("switch_bscreen", Boolean.valueOf(getString(R.string.pref_default_bsceen))));
    }

    public void gotoNext(View view) {
        setPrefs();

        Intent i = new Intent(SetupPgOneActivity.this, SetupPgTwoActivity.class);
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
                        Intent i = new Intent(SetupPgOneActivity.this, DetectorActivity.class);
                        i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);
                        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        startActivity(i);
                    }
                } );
        alertDialog.setButton(AlertDialog.BUTTON_NEGATIVE, "Cancel",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                } );
        alertDialog.show();
    }

    public void gotoPrev(View view) {
        setPrefs();

        Intent i = new Intent(SetupPgOneActivity.this, SetupIntroActivity.class);
        i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(i);
    }

    public void setPrefs() {
        EditText username = (EditText) findViewById(R.id.text_username);
        String text_username = username.getText().toString();
        sharedPreferences.edit().putString("text_username", text_username).apply();

        Switch bscreen = (Switch) findViewById(R.id.switch_bscreen);
        Boolean switch_bscreen = bscreen.isChecked();
        sharedPreferences.edit().putBoolean("switch_bscreen", switch_bscreen).apply();
    }
}