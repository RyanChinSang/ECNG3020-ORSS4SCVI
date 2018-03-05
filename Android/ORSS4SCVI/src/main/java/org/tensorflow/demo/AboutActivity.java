package org.tensorflow.demo;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Point;
import android.os.Bundle;
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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_about);
        setupActionBar();
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
        alertDialog.setTitle("GNU General Public License v3");
        alertDialog.setMessage(formattedText);
        alertDialog.show();
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
}
