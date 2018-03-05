/*
 * TODO (cleanup [HIGH]): Cleanup assets folder
 * TODO ([HIGH]): Create a centralized versioning method
 * TODO ([MED]): Add another view that interacts with pref_about "version" block to get a (formatted) changelog
 *
 */


package org.tensorflow.demo;

import android.annotation.TargetApi;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.preference.EditTextPreference;
import android.preference.ListPreference;
import android.preference.Preference;
import android.preference.PreferenceFragment;
import android.preference.PreferenceManager;
import android.preference.RingtonePreference;
import android.support.v7.app.ActionBar;
import android.text.TextUtils;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;

import java.util.List;

public class SettingsActivity extends AppCompatPreferenceActivity {

    static int pos;
    static String head;
    public static Context contextOfApplication;

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        if (head != null) {
            getMenuInflater().inflate(R.menu.menu_menu_frag, menu);
        } else {
            getMenuInflater().inflate(R.menu.menu_menu_main, menu);
        }
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle item selection
        switch (item.getItemId()) {
            case R.id.home_menu_frag:
                head = null;
                Intent intent_home = new Intent(SettingsActivity.this, DetectorActivity.class);
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

    public void shutDown() {
        stopService(new Intent(SettingsActivity.this, ttsService.class));
        moveTaskToBack(true);
        android.os.Process.killProcess(android.os.Process.myPid());
        System.exit(1);
    }

    @Override
    public void onHeaderClick(Header header, int position) {
        head = header.toString();
        pos = position;

        super.onHeaderClick(header, position);
        if (header.id == R.id.exit_menu) {
            head = null;
            sayTTS("good bye");
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    shutDown();
                }
            },500);
        } else if (header.id == R.id.about) {
            head = null;
        }
    }

    public void sayTTS(String string) {
        SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        boolean tts_mode = sharedPreferences.getBoolean("switch_set_tts", false);
        if (tts_mode) {
            Intent i = new Intent(getApplicationContext(), ttsService.class);
            i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);  // TODO (cleanup): is this necessary?
            i.putExtra("key", string);
            startService(i);
        }
    }

    /**
     * A preference value change listener that updates the preference's summary
     * to reflect its new value.
     */
    private static Preference.OnPreferenceChangeListener sBindPreferenceSummaryToValueListener = new Preference.OnPreferenceChangeListener() {
        @Override
        public boolean onPreferenceChange(Preference preference, Object value) {
            String stringValue = value.toString();

            if (preference instanceof ListPreference) {
                // For list preferences, look up the correct display value in
                // the preference's 'entries' list.
                ListPreference listPreference = (ListPreference) preference;
                int index = listPreference.findIndexOfValue(stringValue);

                // Set the summary to reflect the new value.
                preference.setSummary(
                        index >= 0
                                ? listPreference.getEntries()[index]
                                : null);

            } else if (preference instanceof RingtonePreference) {
                // For ringtone preferences, look up the correct display value
                // using RingtoneManager.
                if (TextUtils.isEmpty(stringValue)) {
                    // Empty values correspond to 'silent' (no ringtone).
                    preference.setSummary(R.string.pref_ringtone_silent);

                } else {
                    Ringtone ringtone = RingtoneManager.getRingtone(
                            preference.getContext(), Uri.parse(stringValue));

                    if (ringtone == null) {
                        // Clear the summary if there was a lookup error.
                        preference.setSummary(null);
                    } else {
                        // Set the summary to reflect the new ringtone display
                        // name.
                        String name = ringtone.getTitle(preference.getContext());
                        preference.setSummary(name);
                    }
                }

            } else {
                // For all other preferences, set the summary to the value's
                // simple string representation.
                preference.setSummary(stringValue);
            }

            return true;
        }
    };

    /**
     * Helper method to determine if the device has an extra-large screen. For
     * example, 10" tablets are extra-large.
     */
    private static boolean isXLargeTablet(Context context) {
        return (context.getResources().getConfiguration().screenLayout
                & Configuration.SCREENLAYOUT_SIZE_MASK) >= Configuration.SCREENLAYOUT_SIZE_XLARGE;
    }

    /**
     * Binds a preference's summary to its value. More specifically, when the
     * preference's value is changed, its summary (line of text below the
     * preference title) is updated to reflect the value. The summary is also
     * immediately updated upon calling this method. The exact display format is
     * dependent on the type of preference.
     *
     * @see #sBindPreferenceSummaryToValueListener
     */
    private static void bindPreferenceSummaryToValue(Preference preference) {
        // Set the listener to watch for value changes.
        preference.setOnPreferenceChangeListener(sBindPreferenceSummaryToValueListener);

        // Trigger the listener immediately with the preference's
        // current value.
        sBindPreferenceSummaryToValueListener.onPreferenceChange(preference,
                PreferenceManager
                        .getDefaultSharedPreferences(preference.getContext())
                        .getString(preference.getKey(), ""));
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        contextOfApplication = getApplicationContext();
        setupActionBar();
    }

    /**
     * Set up the {@link android.app.ActionBar}, if the API is available.
     */
    private void setupActionBar() {
        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            // Show the Up button in the action bar.
            actionBar.setDisplayHomeAsUpEnabled(true);
            actionBar.setHomeButtonEnabled(true);
        }
    }

    @Override
    public boolean onMenuItemSelected(int featureId, MenuItem item) {
        int id = item.getItemId();
        if (id == android.R.id.home) {
            if (head != null) {
                head = null;
                super.onBackPressed();
            } else {
                Intent intent_home = new Intent(SettingsActivity.this, DetectorActivity.class);
                intent_home.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);
                intent_home.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(intent_home);
            }
            return true;
        }
        return super.onMenuItemSelected(featureId, item);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public boolean onIsMultiPane() {
        return isXLargeTablet(this);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    @TargetApi(Build.VERSION_CODES.HONEYCOMB)
    public void onBuildHeaders(List<Header> target) {
        loadHeadersFromResource(R.xml.pref_headers, target);
    }

    /**
     * This method stops fragment injection in malicious applications.
     * Make sure to deny any unknown fragments here.
     */
    protected boolean isValidFragment(String fragmentName) {
        return PreferenceFragment.class.getName().equals(fragmentName)
                || SettingsPreferenceFragment.class.getName().equals(fragmentName);
    }

    /**
     * This fragment shows SETTINGS (GENERAL) preferences only. It is used when the
     * activity is showing a two-pane settings UI.
     */
    @TargetApi(Build.VERSION_CODES.HONEYCOMB)
    public static class SettingsPreferenceFragment extends PreferenceFragment {
        @Override
        public void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            addPreferencesFromResource(R.xml.pref_settings);
            setHasOptionsMenu(true);
            setMenuVisibility(true);
            // Bind the summaries of EditText/List/Dialog/Ringtone preferences
            // to their values. When their values change, their summaries are
            // updated to reflect the new value, per the Android Design
            // guidelines.
            bindPreferenceSummaryToValue(findPreference("text_ROIsize"));
            bindPreferenceSummaryToValue(findPreference("list_set_stt"));

            Preference preference_sw_tts = findPreference("switch_set_tts");
            preference_sw_tts.setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
                @Override
                public boolean onPreferenceClick(Preference preference) {
                    SharedPreferences sharedPref = PreferenceManager.getDefaultSharedPreferences(getActivity());
                    boolean isChecked = sharedPref.getBoolean("switch_set_tts", false);
                    if (isChecked) {
                        Toast.makeText(getActivity().getApplicationContext(), "Text to Speech enabled", Toast.LENGTH_LONG).show();
                    } else {
                        Toast.makeText(getActivity().getApplicationContext(), "Text to Speech disabled", Toast.LENGTH_LONG).show();
                    }
                    return false;
                }
            });

            Preference preference_sw_cols = findPreference("switch_set_cols");
            preference_sw_cols.setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
                @Override
                public boolean onPreferenceClick(Preference preference) {
                    SharedPreferences sharedPref = PreferenceManager.getDefaultSharedPreferences(getActivity());
                    boolean isChecked = sharedPref.getBoolean("switch_set_cols", false);
                    if (isChecked) {
                        Toast.makeText(getActivity().getApplicationContext(), "Using advanced colors", Toast.LENGTH_LONG).show();
                    } else {
                        Toast.makeText(getActivity().getApplicationContext(), "Using simple colors", Toast.LENGTH_LONG).show();
                    }
                    return false;
                }
            });

            Preference preference_sw_filt = findPreference("switch_set_filt");
            preference_sw_filt.setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
                @Override
                public boolean onPreferenceClick(Preference preference) {
                    SharedPreferences sharedPref = PreferenceManager.getDefaultSharedPreferences(getActivity());
                    boolean isChecked = sharedPref.getBoolean("switch_set_filt", false);
                    if (isChecked) {
                        Toast.makeText(getActivity().getApplicationContext(), "Filtering enabled", Toast.LENGTH_LONG).show();
                    } else {
                        Toast.makeText(getActivity().getApplicationContext(), "Filtering disabled", Toast.LENGTH_LONG).show();
                    }
                    return false;
                }
            });

            EditTextPreference editTextPreference = (EditTextPreference) findPreference("text_ROIsize");
            editTextPreference.setOnPreferenceChangeListener(new Preference.OnPreferenceChangeListener() {
                @Override
                public boolean onPreferenceChange(Preference preference, Object newValue) {
                    int val = Integer.parseInt(newValue.toString());
                    if ((val > 0) && (val < 241)) {
                        preference.setSummary(""+val);
                        return true;
                    } else {
                        Toast.makeText(getActivity(), "ERROR: Valid range is 1 to 240 only", Toast.LENGTH_LONG).show();
                        return false;
                    }
                }
            });

            Preference preference_sw_confstr = findPreference("switch_set_confstr");
            preference_sw_confstr.setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
                @Override
                public boolean onPreferenceClick(Preference preference) {
                    SharedPreferences sharedPref = PreferenceManager.getDefaultSharedPreferences(getActivity());
                    boolean isChecked = sharedPref.getBoolean("switch_set_confstr", false);
                    if (isChecked) {
                        Toast.makeText(getActivity().getApplicationContext(), "Using confidence values", Toast.LENGTH_LONG).show();
                    } else {
                        Toast.makeText(getActivity().getApplicationContext(), "Using object name only", Toast.LENGTH_LONG).show();
                    }
                    return false;
                }
            });
        }

        @Override
        public void onResume() {
            super.onResume();
            android.preference.SwitchPreference preference_sw_cols = (android.preference.SwitchPreference) findPreference("switch_set_cols");
            preference_sw_cols.setSummaryOff("Using a list of 10 colors");
            preference_sw_cols.setSummaryOn("Using a list of 628 colors");

            android.preference.SwitchPreference preference_sw_confstr = (android.preference.SwitchPreference) findPreference("switch_set_confstr");
            preference_sw_confstr.setSummaryOff("Outputting object name only");
            preference_sw_confstr.setSummaryOn("Outputting name and confidence");
        }

        @Override
        public boolean onOptionsItemSelected(MenuItem item) {
            int id = item.getItemId();
            if (id == android.R.id.home) {
                startActivity(new Intent(getActivity(), SettingsActivity.class));
                return true;
            }
            return super.onOptionsItemSelected(item);
        }
    }
}
