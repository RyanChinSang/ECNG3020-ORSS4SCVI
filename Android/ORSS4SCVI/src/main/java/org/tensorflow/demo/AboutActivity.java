package org.tensorflow.demo;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Point;
import android.net.Uri;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.text.Html;
import android.text.Spanned;
import android.text.method.LinkMovementMethod;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;

public class AboutActivity extends AppCompatActivity {

    SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_about);
        setupActionBar();
        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        sharedPreferences.edit().putBoolean("uniqueInstance", false).apply();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_menu_frag, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle item selection
        switch (item.getItemId()) {
            case R.id.home_menu_frag:
                Intent intent_home = new Intent(AboutActivity.this, DetectorActivity.class);
                intent_home.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);
                intent_home.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(intent_home);
                return true;
            case android.R.id.home:
                super.onBackPressed();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    private void setupActionBar() {
        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            // Show the Up button in the action bar.
            actionBar.setTitle("About");
            actionBar.setDisplayHomeAsUpEnabled(true);
            actionBar.setHomeButtonEnabled(true);
        }
    }

    public void getChangelog(View view) {
        AlertDialog alertDialog = new AlertDialog.Builder(this).create();
        String formattedText = getString(R.string.version_log);
        Spanned versionLog = Html.fromHtml(formattedText);
        alertDialog.setTitle("Version Changelog");
        alertDialog.setMessage(versionLog);
        alertDialog.show();
        ((TextView)alertDialog.findViewById(android.R.id.message)).setMovementMethod(LinkMovementMethod.getInstance());
        alertDialog.getWindow().setLayout((int)(getScreenWidth(this)*1.), (int)(getScreenHeight(this)*.8));
    }

    public void getLicense(View view) {
        AlertDialog alertDialog = new AlertDialog.Builder(this).create();
        String formattedText = getString(R.string.gnu_license);
        Spanned GNULicence = Html.fromHtml(formattedText);
        alertDialog.setTitle("GNU General Public License");
        alertDialog.setMessage(GNULicence);
        alertDialog.show();
        ((TextView)alertDialog.findViewById(android.R.id.message)).setMovementMethod(LinkMovementMethod.getInstance());
        alertDialog.getWindow().setLayout((int)(getScreenWidth(this)*1.), (int)(getScreenHeight(this)*.8));
    }

    public static int getScreenWidth(Activity activity) {
        Point size = new Point();
        activity.getWindowManager().getDefaultDisplay().getSize(size);
        return size.x;
    }

    public static int getScreenHeight(Activity activity) {
        Point size = new Point();
        activity.getWindowManager().getDefaultDisplay().getSize(size);
        return size.y;
    }

    public void openHome(View view) {
        Intent intent = new Intent();
        intent.setAction(Intent.ACTION_VIEW);
        intent.addCategory(Intent.CATEGORY_BROWSABLE);
        intent.setData(Uri.parse("https://github.com/RyanChinSang/ECNG3020-ORSS4SCVI/tree/master/Android/ORSS4SCVI"));
        startActivity(intent);
    }
}
