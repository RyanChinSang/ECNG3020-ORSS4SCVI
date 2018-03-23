package org.tensorflow.demo;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.Toast;

public class SetupPgTwoActivity extends AppCompatActivity {

    SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_pg_two);

        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        Switch set_filt = (Switch) findViewById(R.id.switch_set_filt);
        set_filt.setChecked(sharedPreferences.getBoolean("switch_set_filt", Boolean.valueOf(getString(R.string.pref_default_set_filt))));

        Switch set_cols = (Switch) findViewById(R.id.switch_set_cols);
        set_cols.setChecked(sharedPreferences.getBoolean("switch_set_cols", Boolean.valueOf(getString(R.string.pref_default_set_cols))));

        EditText ROIsize = (EditText) findViewById(R.id.text_ROIsize);
        ROIsize.setText(sharedPreferences.getString("text_ROIsize", getString(R.string.pref_default_ROIsize)));
        ROIsize.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
            }

            @Override
            public void afterTextChanged(Editable s) {
                if (!s.toString().equals("")) {
                    int val = Integer.parseInt(s.toString());
                    if ((val > 0) && (val < 241)) {
                        EditText ROIsize = (EditText) findViewById(R.id.text_ROIsize);
                        String text_ROIsize = ROIsize.getText().toString();
                        sharedPreferences.edit().putString("text_ROIsize", text_ROIsize).apply();
                    } else {
                        s.replace(0, s.length(), "240");
                        Toast.makeText(getApplicationContext(), "Valid range is 1 to 240 only", Toast.LENGTH_LONG).show();
                    }
                } else {
                    s.replace(0, s.length(), "1");
                    Toast.makeText(getApplicationContext(), "Valid range is 1 to 240 only", Toast.LENGTH_LONG).show();
                }
            }
        });
    }

    public void gotoNext(View view) {
        setPrefs();

        Intent i = new Intent(SetupPgTwoActivity.this, SetupPgThreeActivity.class);
        i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(i);
    }

    public void gotoSkip(View view) {
        AlertDialog alertDialog = new AlertDialog.Builder(this).create();
        alertDialog.setTitle("Skip Setup?");
        alertDialog.setMessage(getString(R.string.setup_skip_message));
        alertDialog.setButton(AlertDialog.BUTTON_POSITIVE, "OK",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        Intent i = new Intent(SetupPgTwoActivity.this, DetectorActivity.class);
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

        Intent i = new Intent(SetupPgTwoActivity.this, SetupPgOneActivity.class);
        i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(i);
    }

    public void setPrefs() {
        Switch set_filt = (Switch) findViewById(R.id.switch_set_filt);
        Boolean switch_set_filt = set_filt.isChecked();
        sharedPreferences.edit().putBoolean("switch_set_filt", switch_set_filt).apply();

        Switch set_cols = (Switch) findViewById(R.id.switch_set_cols);
        Boolean switch_set_cols = set_cols.isChecked();
        sharedPreferences.edit().putBoolean("switch_set_cols", switch_set_cols).apply();

        EditText ROIsize = (EditText) findViewById(R.id.text_ROIsize);
        String text_ROIsize = ROIsize.getText().toString();
        sharedPreferences.edit().putString("text_ROIsize", text_ROIsize).apply();
    }
}