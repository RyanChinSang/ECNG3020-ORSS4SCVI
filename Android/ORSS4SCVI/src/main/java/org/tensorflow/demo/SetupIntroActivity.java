package org.tensorflow.demo;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.TextView;

public class SetupIntroActivity extends AppCompatActivity {

    SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_intro);

        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        TextView textView = (TextView) findViewById(R.id.tv_intro_desc);
        String string = "Hello there! @nl @nl I am your assistant for the ORSS4SCVI. @nl @nl This is a setup wizard that will help you quickly configure your Application to your own liking.";
        string = string.replaceAll("@nl", System.getProperty("line.separator"));
        textView.setText(string);
    }

    public void gotoNext(View view) {
        Intent i = new Intent(SetupIntroActivity.this, SetupPgOneActivity.class);
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
                        Intent i = new Intent(SetupIntroActivity.this, DetectorActivity.class);
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
}
