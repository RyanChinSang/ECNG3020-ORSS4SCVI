package org.tensorflow.demo;

import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.preference.EditTextPreference;
import android.preference.ListPreference;
import android.preference.Preference;
import android.preference.PreferenceFragment;
import android.preference.PreferenceManager;
import android.support.v7.app.ActionBar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;

import java.util.List;

public class SettingsActivity extends AppCompatPreferenceActivity {

    /*[MY VARIABLES]*******************************************************************************/
    public static Activity activity = null;
    static int pos;
    static String head;
    SharedPreferences sharedPreferences;
    public static Context contextOfApplication;


    /*[DEFAULT FUNCTIONS]**************************************************************************/
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

    @Override
    public void onHeaderClick(Header header, int position) {
        head = header.toString();
        pos = position;

        super.onHeaderClick(header, position);
        if (header.id == R.id.exit_menu) {
            head = null;
            communicate("Good bye", getApplicationContext());
            shutDown();
        } else if (header.id == R.id.about) {
            head = null;
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
        activity = this;
        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        sharedPreferences.edit().putBoolean("uniqueInstance", false).apply();
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
                sharedPreferences.edit().putBoolean("uniqueInstance", false).apply();
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


    /*[SETTINGS (GENERAL)]*************************************************************************/
    @TargetApi(Build.VERSION_CODES.HONEYCOMB)
    public static class SettingsPreferenceFragment extends PreferenceFragment {
        @Override
        public void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            addPreferencesFromResource(R.xml.pref_settings);
            setHasOptionsMenu(true);
            setMenuVisibility(true);
            final SharedPreferences sharedPref = PreferenceManager.getDefaultSharedPreferences(getActivity());
            // Bind the summaries of EditText/List/Dialog/Ringtone preferences
            // to their values. When their values change, their summaries are
            // updated to reflect the new value, per the Android Design
            // guidelines.
            bindPreferenceSummaryToValue(findPreference("text_username"));
            bindPreferenceSummaryToValue(findPreference("text_ROIsize"));
            bindPreferenceSummaryToValue(findPreference("list_set_stt"));

            Preference preference_sw_tts = findPreference("switch_set_tts");
            preference_sw_tts.setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
                @Override
                public boolean onPreferenceClick(Preference preference) {
                    boolean isChecked = sharedPref.getBoolean("switch_set_tts", false);
                    if (isChecked) {
                        communicate("Text to Speech enabled", getActivity().getApplicationContext());
                    } else {
                        communicate("Text to Speech disabled", getActivity().getApplicationContext());
                    }
                    return false;
                }
            });

            Preference preference_sw_cols = findPreference("switch_set_cols");
            preference_sw_cols.setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
                @Override
                public boolean onPreferenceClick(Preference preference) {
                    boolean isChecked = sharedPref.getBoolean("switch_set_cols", false);
                    if (isChecked) {
                        communicate("Using advanced colors", getActivity().getApplicationContext());
                    } else {
                        communicate("Using simple colors", getActivity().getApplicationContext());
                    }
                    return false;
                }
            });

            Preference preference_sw_filt = findPreference("switch_set_filt");
            preference_sw_filt.setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
                @Override
                public boolean onPreferenceClick(Preference preference) {
                    boolean isChecked = sharedPref.getBoolean("switch_set_filt", false);
                    if (isChecked) {
                        communicate("Filtering enabled", getActivity().getApplicationContext());
                    } else {
                        communicate("Filtering disabled", getActivity().getApplicationContext());
                    }
                    return false;
                }
            });

            EditTextPreference preference_tx_ROIsize = (EditTextPreference) findPreference("text_ROIsize");
            preference_tx_ROIsize.setOnPreferenceChangeListener(new Preference.OnPreferenceChangeListener() {
                @Override
                public boolean onPreferenceChange(Preference preference, Object newValue) {
                    int val = Integer.parseInt(newValue.toString());
                    // TODO (medium): get upperbound to this value: ((1/2 * horizontal resolution) + 1) how to get horiz. res?
                    if ((val > 0) && (val < 241)) {
                        preference.setSummary(""+val);
                        communicate("R.O.I. size changed to "+val+" pixels", getActivity().getApplicationContext());
                        return true;
                    } else {
                        communicate("ERROR. Valid range is 1 to 240 only", getActivity().getApplicationContext());
                        return false;
                    }
                }
            });

            Preference preference_sw_confstr = findPreference("switch_set_confstr");
            preference_sw_confstr.setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
                @Override
                public boolean onPreferenceClick(Preference preference) {
                    boolean isChecked = sharedPref.getBoolean("switch_set_confstr", false);
                    if (isChecked) {
                        communicate("Using confidence values", getActivity().getApplicationContext());
                    } else {
                        communicate("Using object name only", getActivity().getApplicationContext());
                    }
                    return false;
                }
            });

            Preference preference_sw_bscreen= findPreference("switch_bscreen");
            preference_sw_bscreen.setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
                @Override
                public boolean onPreferenceClick(Preference preference) {
                    boolean isChecked = sharedPref.getBoolean("switch_bscreen", false);
                    if (isChecked) {
                        communicate("Black-screen operation allowed", getActivity().getApplicationContext());
                    } else {
                        communicate("Black-screen operation dis-allowed", getActivity().getApplicationContext());
                    }
                    return false;
                }
            });

            EditTextPreference preference_tx_username = (EditTextPreference) findPreference("text_username");
            if (preference_tx_username.getText().equals(null) || preference_tx_username.getText().equals("")) {
                preference_tx_username.setSummary(getString(R.string.pref_title_username_hint));
            }
            preference_tx_username.setOnPreferenceChangeListener(new Preference.OnPreferenceChangeListener() {
                @Override
                public boolean onPreferenceChange(Preference preference, Object newValue) {
                    String username = newValue.toString();
                    if (username.equals(null) || username.equals("")) {
                        preference.setSummary(getString(R.string.pref_title_username_hint));
                        communicate("Username is set to default", getActivity().getApplicationContext());
                    } else {
                        preference.setSummary(username);
                        communicate("Username is set to "+username, getActivity().getApplicationContext());
                    }
                    return true;
                }
            });

            ListPreference preference_li_reset = (ListPreference) findPreference("list_reset");
            preference_li_reset.setOnPreferenceChangeListener(new Preference.OnPreferenceChangeListener() {
                @Override
                public boolean onPreferenceChange(Preference preference, Object newValue) {
                    communicate("Reset successful", getActivity().getApplicationContext());
                    sharedPref.edit().putBoolean("initRun", true).apply();
                    sharedPref.edit().putString("text_username", getString(R.string.pref_default_username)).apply();
                    sharedPref.edit().putBoolean("switch_bscreen", Boolean.valueOf(getString(R.string.pref_default_bsceen))).apply();
                    sharedPref.edit().putBoolean("switch_set_filt", Boolean.valueOf(getString(R.string.pref_default_set_filt))).apply();
                    sharedPref.edit().putBoolean("switch_set_cols", Boolean.valueOf(getString(R.string.pref_default_set_cols))).apply();
                    sharedPref.edit().putString("text_ROIsize", getString(R.string.pref_default_ROIsize)).apply();
                    sharedPref.edit().putBoolean("switch_set_confstr", Boolean.valueOf(getString(R.string.pref_default_set_confstr))).apply();
                    sharedPref.edit().putBoolean("switch_set_tts", Boolean.valueOf(getString(R.string.pref_default_set_tts))).apply();
                    sharedPref.edit().putString("list_set_stt", getString(R.string.pref_default_set_stt)).apply();
                    sharedPref.edit().remove("list_set_stt_setup").apply();
                    new Handler().postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            Intent i = new Intent(contextOfApplication, DetectorActivity.class);
                            i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP|Intent.FLAG_ACTIVITY_NEW_TASK);
                            startActivity(i);
                        }
                    },1125);
                    return true;
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


    /*[OTHER]**************************************************************************************/
    public void shutDown() {
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                sharedPreferences.edit().putBoolean("uniqueInstance", true).apply();
                finishAffinity();
            }
        },600);
    }

    static public void sayTTS(String string, Context context) {
        if (context != null) {
            Intent i = new Intent(context, ttsService.class);
            i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            i.putExtra("key", string);
            context.startService(i);
        }
    }

    static public void communicate(String message, Context context) {
        if (context != null) {
            Toast.makeText(context, message, Toast.LENGTH_LONG).show();
            sayTTS(message, context);
        }
    }
}
