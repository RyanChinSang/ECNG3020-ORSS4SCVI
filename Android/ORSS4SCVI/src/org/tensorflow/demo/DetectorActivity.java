/* DA
 * TODO (fix [HIGH]): App does not return to camera view when the app is reopened from minimized after the settings menu is accessed
 */

package org.tensorflow.demo;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.Bitmap.Config;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.Paint.Style;
import android.graphics.RectF;
import android.graphics.Typeface;
import android.media.ImageReader.OnImageAvailableListener;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.preference.PreferenceManager;
import android.support.v7.app.AlertDialog;
import android.util.Log;
import android.util.Size;
import android.util.TypedValue;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import com.vikramezhil.droidspeech.DroidSpeech;
import com.vikramezhil.droidspeech.OnDSListener;
import com.vikramezhil.droidspeech.OnDSPermissionsListener;

import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;
import org.tensorflow.demo.OverlayView.DrawCallback;
import org.tensorflow.demo.env.BorderedText;
import org.tensorflow.demo.env.ImageUtils;
import org.tensorflow.demo.env.Logger;
import org.tensorflow.demo.tracking.MultiBoxTracker;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Vector;

import edu.cmu.pocketsphinx.Assets;
import edu.cmu.pocketsphinx.Hypothesis;
import edu.cmu.pocketsphinx.RecognitionListener;
import edu.cmu.pocketsphinx.SpeechRecognizer;
import edu.cmu.pocketsphinx.SpeechRecognizerSetup;

import static edu.cmu.pocketsphinx.SpeechRecognizerSetup.defaultSetup;


/**
 * An activity that uses a TensorFlowMultiBoxDetector and ObjectTracker to detect and then track
 * objects.
 */
public class DetectorActivity extends CameraActivity implements OnImageAvailableListener, OnDSListener, OnDSPermissionsListener {

    /*[TF VARIABLES]*******************************************************************************/
    private static final float TEXT_SIZE_DIP = 10;
    private static final int TF_OD_API_INPUT_SIZE = 300;
    private static final boolean SAVE_PREVIEW_BITMAP = false;
    private static final float MINIMUM_CONFIDENCE_TF_OD_API = 0.6f;
    private static final DetectorMode MODE = DetectorMode.TF_OD_API;
    private static final boolean MAINTAIN_ASPECT = MODE == DetectorMode.YOLO;
    private static final Size DESIRED_PREVIEW_SIZE = new Size(640, 480);
    private static final String TF_OD_API_LABELS_FILE = "file:///android_asset/coco_labels_list.txt";
    private static final String TF_OD_API_MODEL_FILE = "file:///android_asset/ssd_mobilenet_v1_android_export.pb";
    private long timestamp = 0;
    private enum DetectorMode {
        TF_OD_API,
        YOLO;
    }
    private Bitmap croppedBitmap = null;
    private Bitmap rgbFrameBitmap = null;
    private Bitmap cropCopyBitmap = null;
    private boolean computingDetection = false;
    private static final Logger LOGGER = new Logger();
    OverlayView trackingOverlay;
    private Classifier detector;
    private byte[] luminanceCopy;
    private MultiBoxTracker tracker;
    private BorderedText borderedText;
    private Integer sensorOrientation;
    private long lastProcessingTimeMs;
    private Matrix frameToCropTransform;
    private Matrix cropToFrameTransform;


    /*[MY VARIABLES]*******************************************************************************/
    private static final String KWS_SEARCH = "wakeup";
    private static final String KEYPHRASE = "ok assistant";
    ArrayList<String> detectedObjects = new ArrayList<String>();
    private static final Map<String, String> cols_dict = new LinkedHashMap<String, String>() {{
        put("84;84;84", "Grey");
        put("192;192;192", "Silver");
        put("190;190;190", "grey");
        put("211;211;211", "Light Gray");
        put("119;136;153", "Light Slate Grey");
        put("112;128;144", "Slate Gray");
        put("198;226;255", "Slate Gray 1");
        put("185;211;238", "Slate Gray 2");
        put("159;182;205", "Slate Gray 3");
        put("108;123;139", "Slate Gray 4");
        put("0;0;0", "black");
        put("1;1;1", "grey 0");
        put("3;3;3", "grey 1");
        put("5;5;5", "grey 2");
        put("8;8;8", "grey 3");
        put("10;10;10", "grey 4");
        put("13;13;13", "grey 5");
        put("15;15;15", "grey 6");
        put("18;18;18", "grey 7");
        put("20;20;20", "grey 8");
        put("23;23;23", "grey 9");
        put("26;26;26", "grey 10");
        put("28;28;28", "grey 11");
        put("31;31;31", "grey 12");
        put("33;33;33", "grey 13");
        put("36;36;36", "grey 14");
        put("38;38;38", "grey 15");
        put("41;41;41", "grey 16");
        put("43;43;43", "grey 17");
        put("46;46;46", "grey 18");
        put("48;48;48", "grey 19");
        put("51;51;51", "grey 20");
        put("54;54;54", "grey 21");
        put("56;56;56", "grey 22");
        put("59;59;59", "grey 23");
        put("61;61;61", "grey 24");
        put("64;64;64", "grey 25");
        put("66;66;66", "grey 26");
        put("69;69;69", "grey 27");
        put("71;71;71", "grey 28");
        put("74;74;74", "grey 29");
        put("77;77;77", "grey 30");
        put("79;79;79", "grey 31");
        put("82;82;82", "grey 32");
        put("85;85;85", "grey 33");
        put("87;87;87", "grey 34");
        put("89;89;89", "grey 35");
        put("92;92;92", "grey 36");
        put("94;94;94", "grey 37");
        put("97;97;97", "grey 38");
        put("99;99;99", "grey 39");
        put("102;102;102", "grey 40");
        put("105;105;105", "Dim Grey");
        put("107;107;107", "grey 42");
        put("110;110;110", "grey 43");
        put("112;112;112", "grey 44");
        put("115;115;115", "grey 45");
        put("117;117;117", "grey 46");
        put("120;120;120", "grey 47");
        put("122;122;122", "grey 48");
        put("125;125;125", "grey 49");
        put("127;127;127", "grey 50");
        put("130;130;130", "grey 51");
        put("133;133;133", "grey 52");
        put("135;135;135", "grey 53");
        put("138;138;138", "grey 54");
        put("140;140;140", "grey 55");
        put("143;143;143", "grey 56");
        put("145;145;145", "grey 57");
        put("148;148;148", "grey 58");
        put("150;150;150", "grey 59");
        put("153;153;153", "grey 60");
        put("156;156;156", "grey 61");
        put("158;158;158", "grey 62");
        put("161;161;161", "grey 63");
        put("163;163;163", "grey 64");
        put("166;166;166", "grey 65");
        put("168;168;168", "grey 66");
        put("171;171;171", "grey 67");
        put("173;173;173", "grey 68");
        put("176;176;176", "grey 69");
        put("179;179;179", "grey 70");
        put("181;181;181", "grey 71");
        put("184;184;184", "grey 72");
        put("186;186;186", "grey 73");
        put("189;189;189", "grey 74");
        put("191;191;191", "grey 75");
        put("194;194;194", "grey 76");
        put("196;196;196", "grey 77");
        put("199;199;199", "grey 78");
        put("201;201;201", "grey 79");
        put("204;204;204", "grey 80");
        put("207;207;207", "grey 81");
        put("209;209;209", "grey 82");
        put("212;212;212", "grey 83");
        put("214;214;214", "grey 84");
        put("217;217;217", "grey 85");
        put("219;219;219", "grey 86");
        put("222;222;222", "grey 87");
        put("224;224;224", "grey 88");
        put("227;227;227", "grey 89");
        put("229;229;229", "grey 90");
        put("232;232;232", "grey 91");
        put("235;235;235", "grey 92");
        put("237;237;237", "grey 93");
        put("240;240;240", "grey 94");
        put("242;242;242", "grey 95");
        put("245;245;245", "grey 96");
        put("247;247;247", "grey 97");
        put("250;250;250", "grey 98");
        put("252;252;252", "grey 99");
        put("255;255;255", "White");
        put("47;79;79", "Dark Slate Grey");
        put("86;86;86", "Dim Grey");
        put("205;205;205", "Very Light Grey");
        put("99;86;136", "Free Speech Grey");
        put("240;248;255", "Alice Blue");
        put("138;43;226", "Blue Violet");
        put("95;159;159", "Cadet Blue");
        put("95;158;160", "Cadet Blue");
        put("96;159;161", "Cadet Blue");
        put("152;245;255", "Cadet Blue 1");
        put("142;229;238", "Cadet Blue 2");
        put("122;197;205", "Cadet Blue 3");
        put("83;134;139", "Cadet Blue 4");
        put("66;66;111", "Corn Flower Blue");
        put("100;149;237", "Cornflower Blue");
        put("72;61;139", "Dark Slate Blue");
        put("0;206;209", "Dark Turquoise");
        put("0;191;255", "Deep Sky Blue");
        put("1;192;254", "Deep Sky Blue 1");
        put("0;178;238", "Deep Sky Blue 2");
        put("0;154;205", "Deep Sky Blue 3");
        put("0;104;139", "Deep Sky Blue 4");
        put("30;144;255", "Dodger Blue");
        put("31;145;254", "Dodger Blue 1");
        put("28;134;238", "Dodger Blue 2");
        put("24;116;205", "Dodger Blue 3");
        put("16;78;139", "Dodger Blue 4");
        put("173;216;230", "Light Blue");
        put("191;239;255", "Light Blue 1");
        put("178;223;238", "Light Blue 2");
        put("154;192;205", "Light Blue 3");
        put("104;131;139", "Light Blue 4");
        put("224;255;255", "Light Cyan");
        put("225;254;254", "Light Cyan 1");
        put("209;238;238", "Light Cyan 2");
        put("180;205;205", "Light Cyan 3");
        put("122;139;139", "Light Cyan 4");
        put("135;206;250", "Light Sky Blue");
        put("176;226;255", "Light Sky Blue 1");
        put("164;211;238", "Light Sky Blue 2");
        put("141;182;205", "Light Sky Blue 3");
        put("96;123;139", "Light Sky Blue 4");
        put("132;112;255", "Light Slate Blue");
        put("176;196;222", "Light Steel Blue");
        put("202;225;255", "Light Steel Blue 1");
        put("188;210;238", "Light Steel Blue 2");
        put("162;181;205", "Light Steel Blue 3");
        put("110;123;139", "Light Steel Blue 4");
        put("112;219;147", "Aquamarine");
        put("0;0;205", "Medium Blue");
        put("123;104;238", "Medium Slate Blue");
        put("72;209;204", "Medium Turquoise");
        put("25;25;112", "Midnight Blue");
        put("0;0;128", "Navy Blue");
        put("175;238;238", "Pale Turquoise");
        put("187;255;255", "Pale Turquoise 1");
        put("174;238;238", "Pale Turquoise 2");
        put("150;205;205", "Pale Turquoise 3");
        put("102;139;139", "Pale Turquoise 4");
        put("176;224;230", "Powder Blue");
        put("65;105;225", "Royal Blue");
        put("72;118;255", "Royal Blue 1");
        put("67;110;238", "Royal Blue 2");
        put("58;95;205", "Royal Blue 3");
        put("39;64;139", "Royal Blue 4");
        put("0;34;102", "Royal Blue 5");
        put("135;206;235", "Sky Blue");
        put("135;206;255", "Sky Blue 1");
        put("126;192;238", "Sky Blue 2");
        put("108;166;205", "Sky Blue 3");
        put("74;112;139", "Sky Blue 4");
        put("106;90;205", "Slate Blue");
        put("131;111;255", "Slate Blue 1");
        put("122;103;238", "Slate Blue 2");
        put("105;89;205", "Slate Blue 3");
        put("71;60;139", "Slate Blue 4");
        put("70;130;180", "Steel Blue");
        put("99;184;255", "Steel Blue 1");
        put("92;172;238", "Steel Blue 2");
        put("79;148;205", "Steel Blue 3");
        put("54;100;139", "Steel Blue 4");
        put("127;255;212", "aquamarine");
        put("128;254;213", "aquamarine 1");
        put("118;238;198", "aquamarine 2");
        put("102;205;170", "Medium Aquamarine");
        put("69;139;116", "aquamarine 4");
        put("240;255;255", "azure");
        put("241;254;254", "azure 1");
        put("224;238;238", "azure 2");
        put("193;205;205", "azure 3");
        put("131;139;139", "azure 4");
        put("0;0;255", "blue");
        put("1;1;254", "blue 1");
        put("0;0;238", "blue 2");
        put("1;1;206", "blue 3");
        put("0;0;139", "blue 4");
        put("0;255;255", "aqua");
        put("1;254;254", "cyan");
        put("2;255;255", "cyan 1");
        put("0;238;238", "cyan 2");
        put("0;205;205", "cyan 3");
        put("0;139;139", "cyan 4");
        put("1;1;129", "navy");
        put("0;128;128", "teal");
        put("64;224;208", "turquoise");
        put("0;245;255", "turquoise 1");
        put("0;229;238", "turquoise 2");
        put("0;197;205", "turquoise 3");
        put("0;134;139", "turquoise 4");
        put("48;80;80", "Dark Slate Gray");
        put("151;255;255", "Dark Slate Gray 1");
        put("141;238;238", "Dark Slate Gray 2");
        put("121;205;205", "Dark Slate Gray 3");
        put("82;139;139", "Dark Slate Gray 4");
        put("36;24;130", "Dark Slate Blue");
        put("112;147;219", "Dark Turquoise");
        put("127;0;255", "Medium Slate Blue");
        put("112;219;219", "Medium Turquoise");
        put("47;47;79", "Midnight Blue");
        put("35;35;142", "Navy Blue");
        put("77;77;255", "Neon Blue");
        put("0;0;156", "New Midnight Blue");
        put("89;89;171", "Rich Blue");
        put("50;153;204", "Sky Blue");
        put("0;127;255", "Slate Blue");
        put("56;176;222", "Summer Sky");
        put("3;180;200", "Iris Blue");
        put("65;86;197", "Free Speech Blue");
        put("188;143;143", "Rosy Brown");
        put("255;193;193", "Rosy Brown 1");
        put("238;180;180", "Rosy Brown 2");
        put("205;155;155", "Rosy Brown 3");
        put("139;105;105", "Rosy Brown 4");
        put("139;69;19", "Saddle Brown");
        put("244;164;96", "Sandy Brown");
        put("245;245;220", "beige");
        put("165;42;42", "brown");
        put("166;42;42", "brown");
        put("255;64;64", "brown 1");
        put("238;59;59", "brown 2");
        put("205;51;51", "brown 3");
        put("139;35;35", "brown 4");
        put("92;64;51", "dark brown");
        put("222;184;135", "burly wood");
        put("255;211;155", "burly wood 1");
        put("238;197;145", "burly wood 2");
        put("205;170;125", "burly wood 3");
        put("139;115;85", "burly wood 4");
        put("92;51;23", "baker's chocolate");
        put("210;105;30", "chocolate");
        put("255;127;36", "chocolate 1");
        put("238;118;33", "chocolate 2");
        put("205;102;29", "chocolate 3");
        put("140;70;20", "chocolate 4");
        put("205;133;63", "peru");
        put("210;180;140", "tan");
        put("255;165;79", "tan 1");
        put("238;154;73", "tan 2");
        put("206;134;64", "tan 3");
        put("139;90;43", "tan 4");
        put("151;105;79", "Dark Tan");
        put("133;94;66", "Dark Wood");
        put("133;99;99", "Light Wood");
        put("166;128;100", "Medium Wood");
        put("235;199;158", "New Tan");
        put("107;66;38", "Semi Sweet Chocolate");
        put("142;107;35", "Sienna");
        put("219;147;112", "Tan");
        put("93;65;52", "Very Dark Brown");
        put("47;79;47", "Dark Green");
        put("0;100;0", "Dark Green");
        put("74;118;110", "dark green copper");
        put("189;183;107", "Dark Khaki");
        put("85;107;47", "Dark Olive Green");
        put("202;255;112", "Dark Olive Green 1");
        put("188;238;104", "Dark Olive Green 2");
        put("162;205;90", "Dark Olive Green 3");
        put("110;139;61", "Dark Olive Green 4");
        put("128;128;0", "olive");
        put("143;188;143", "Dark Sea Green");
        put("193;255;193", "Dark Sea Green 1");
        put("180;238;180", "Dark Sea Green 2");
        put("155;205;155", "Dark Sea Green 3");
        put("105;139;105", "Dark Sea Green 4");
        put("34;139;34", "Forest Green");
        put("173;255;47", "Green Yellow");
        put("124;252;0", "Lawn Green");
        put("32;178;170", "Light Sea Green");
        put("50;205;50", "Lime Green");
        put("60;179;113", "Medium Sea Green");
        put("0;250;154", "Medium Spring Green");
        put("245;255;250", "Mint Cream");
        put("107;142;35", "Olive Drab");
        put("192;255;62", "Olive Drab 1");
        put("179;238;58", "Olive Drab 2");
        put("154;205;50", "Olive Drab 3");
        put("105;139;34", "Olive Drab 4");
        put("152;251;152", "Pale Green");
        put("154;255;154", "Pale Green 1");
        put("144;238;144", "Pale Green 2");
        put("124;205;124", "Pale Green 3");
        put("84;139;84", "Pale Green 4");
        put("46;139;87", "Sea Green 4");
        put("84;255;159", "Sea Green 1");
        put("78;238;148", "Sea Green 2");
        put("67;205;128", "Sea Green 3");
        put("0;255;127", "Spring Green");
        put("1;254;128", "Spring Green 1");
        put("0;238;118", "Spring Green 2");
        put("0;205;102", "Spring Green 3");
        put("0;139;69", "Spring Green 4");
        put("155;206;51", "Yellow Green");
        put("127;255;0", "chartreuse");
        put("128;254;1", "chartreuse 1");
        put("118;238;0", "chartreuse 2");
        put("102;205;0", "chartreuse 3");
        put("69;139;0", "chartreuse 4");
        put("0;255;0", "green");
        put("0;128;0", "green");
        put("1;254;1", "lime");
        put("2;255;2", "green 1");
        put("0;238;0", "green 2");
        put("0;205;0", "green 3");
        put("0;139;0", "green 4");
        put("240;230;140", "khaki");
        put("255;246;143", "khaki 1");
        put("238;230;133", "khaki 2");
        put("205;198;115", "khaki 3");
        put("139;134;78", "khaki 4");
        put("79;79;47", "Dark Olive Green");
        put("35;142;35", "Medium Aquamarine");
        put("219;219;112", "Medium Forest Green");
        put("66;111;66", "Medium Sea Green");
        put("129;255;2", "Medium Spring Green");
        put("144;189;144", "Pale Green");
        put("35;142;104", "Sea Green");
        put("2;255;129", "Spring Green");
        put("9;249;17", "Free Speech Green");
        put("2;157;116", "Aquamarine");
        put("255;140;0", "Dark Orange");
        put("255;127;0", "Dark Orange 1");
        put("238;118;0", "Dark Orange 2");
        put("205;102;0", "Dark Orange 3");
        put("139;69;0", "Dark Orange 4");
        put("233;150;122", "Dark Salmon");
        put("240;128;128", "Light Coral");
        put("255;160;122", "Light Salmon");
        put("254;161;123", "Light Salmon 1");
        put("238;149;114", "Light Salmon 2");
        put("205;129;98", "Light Salmon 3");
        put("139;87;66", "Light Salmon 4");
        put("255;218;185", "Peach Puff");
        put("254;219;186", "Peach Puff 1");
        put("238;203;173", "Peach Puff 2");
        put("205;175;149", "Peach Puff 3");
        put("139;119;101", "Peach Puff 4");
        put("255;228;196", "bisque");
        put("254;229;197", "bisque 1");
        put("238;213;183", "bisque 2");
        put("205;183;158", "bisque 3");
        put("139;125;107", "bisque 4");
        put("254;128;1", "coral");
        put("255;127;80", "coral");
        put("255;114;86", "coral 1");
        put("238;106;80", "coral 2");
        put("205;91;69", "coral 3");
        put("139;62;47", "coral 4");
        put("240;255;240", "honeydew");
        put("241;254;241", "honeydew 1");
        put("224;238;224", "honeydew 2");
        put("193;205;193", "honeydew 3");
        put("131;139;131", "honeydew 4");
        put("255;165;0", "orange");
        put("254;166;1", "orange 1");
        put("238;154;0", "orange 2");
        put("205;133;0", "orange 3");
        put("139;90;0", "orange 4");
        put("250;128;114", "salmon");
        put("255;140;105", "salmon 1");
        put("238;130;98", "salmon 2");
        put("205;112;84", "salmon 3");
        put("139;76;57", "salmon 4");
        put("160;82;45", "sienna");
        put("255;130;71", "sienna 1");
        put("238;121;66", "sienna 2");
        put("205;104;57", "sienna 3");
        put("139;71;38", "sienna 4");
        put("142;35;35", "Mandarian Orange");
        put("255;129;2", "Orange");
        put("255;36;0", "Orange Red");
        put("255;20;147", "Deep Pink");
        put("254;21;148", "Deep Pink 1");
        put("238;18;137", "Deep Pink 2");
        put("205;16;118", "Deep Pink 3");
        put("139;10;80", "Deep Pink 4");
        put("255;105;180", "Hot Pink");
        put("255;110;180", "Hot Pink 1");
        put("238;106;167", "Hot Pink 2");
        put("205;96;144", "Hot Pink 3");
        put("139;58;98", "Hot Pink 4");
        put("205;92;92", "Indian Red");
        put("255;106;106", "Indian Red 1");
        put("238;99;99", "Indian Red 2");
        put("205;85;85", "Indian Red 3");
        put("139;58;58", "Indian Red 4");
        put("255;182;193", "Light Pink");
        put("255;174;185", "Light Pink 1");
        put("238;162;173", "Light Pink 2");
        put("205;140;149", "Light Pink 3");
        put("139;95;101", "Light Pink 4");
        put("199;21;133", "Medium Violet Red");
        put("255;228;225", "Misty Rose");
        put("254;229;226", "Misty Rose 1");
        put("238;213;210", "Misty Rose 2");
        put("205;183;181", "Misty Rose 3");
        put("139;125;123", "Misty Rose 4");
        put("255;69;0", "Orange Red");
        put("254;70;1", "Orange Red 1");
        put("238;64;0", "Orange Red 2");
        put("205;55;0", "Orange Red 3");
        put("139;37;0", "Orange Red 4");
        put("219;112;147", "Pale Violet Red");
        put("255;130;171", "Pale Violet Red 1");
        put("238;121;159", "Pale Violet Red 2");
        put("205;104;137", "Pale Violet Red 3");
        put("139;71;93", "Pale Violet Red 4");
        put("208;32;144", "Violet Red");
        put("255;62;150", "Violet Red 1");
        put("238;58;140", "Violet Red 2");
        put("205;50;120", "Violet Red 3");
        put("139;34;82", "Violet Red 4");
        put("178;34;34", "firebrick");
        put("255;48;48", "firebrick 1");
        put("238;44;44", "firebrick 2");
        put("205;38;38", "firebrick 3");
        put("139;26;26", "firebrick 4");
        put("255;192;203", "pink");
        put("255;181;197", "pink 1");
        put("238;169;184", "pink 2");
        put("205;145;158", "pink 3");
        put("139;99;108", "pink 4");
        put("245;204;176", "Flesh");
        put("209;146;117", "Feldspar");
        put("255;0;0", "red");
        put("254;1;1", "red 1");
        put("238;0;0", "red 2");
        put("205;0;0", "red 3");
        put("139;0;0", "red 4");
        put("255;99;71", "tomato");
        put("254;100;72", "tomato 1");
        put("238;92;66", "tomato 2");
        put("205;79;57", "tomato 3");
        put("139;54;38", "tomato 4");
        put("134;100;100", "Dusty Rose");
        put("143;36;36", "Firebrick");
        put("246;205;177", "Indian Red");
        put("189;144;144", "Pink");
        put("111;66;66", "Salmon");
        put("140;23;23", "Scarlet");
        put("255;28;174", "Spicy Pink");
        put("227;91;216", "Free Speech Magenta");
        put("192;0;0", "Free Speech Red");
        put("153;50;204", "Dark Orchid");
        put("191;62;255", "Dark Orchid 1");
        put("178;58;238", "Dark Orchid 2");
        put("154;50;205", "Dark Orchid 3");
        put("104;34;139", "Dark Orchid 4");
        put("148;0;211", "Dark Violet");
        put("255;240;245", "Lavender Blush");
        put("254;241;246", "Lavender Blush 1");
        put("238;224;229", "Lavender Blush 2");
        put("205;193;197", "Lavender Blush 3");
        put("139;131;134", "Lavender Blush 4");
        put("186;85;211", "Medium Orchid");
        put("224;102;255", "Medium Orchid 1");
        put("209;95;238", "Medium Orchid 2");
        put("180;82;205", "Medium Orchid 3");
        put("122;55;139", "Medium Orchid 4");
        put("147;112;219", "Medium Purple");
        put("148;113;220", "Medium Orchid");
        put("171;130;255", "Medium Purple 1");
        put("153;50;205", "Dark Orchid");
        put("159;121;238", "Medium Purple 2");
        put("137;104;205", "Medium Purple 3");
        put("93;71;139", "Medium Purple 4");
        put("230;230;250", "lavender");
        put("255;0;255", "magenta");
        put("254;1;254", "fuchsia");
        put("255;2;255", "magenta 1");
        put("238;0;238", "magenta 2");
        put("205;0;205", "magenta 3");
        put("139;0;139", "magenta 4");
        put("176;48;96", "maroon");
        put("255;52;179", "maroon 1");
        put("238;48;167", "maroon 2");
        put("205;41;144", "maroon 3");
        put("139;28;98", "maroon 4");
        put("218;112;214", "orchid");
        put("219;112;219", "Orchid");
        put("255;131;250", "orchid 1");
        put("238;122;233", "orchid 2");
        put("205;105;201", "orchid 3");
        put("139;71;137", "orchid 4");
        put("221;160;221", "plum");
        put("255;187;255", "plum 1");
        put("238;174;238", "plum 2");
        put("205;150;205", "plum 3");
        put("139;102;139", "plum 4");
        put("160;32;240", "purple");
        put("128;0;128", "purple");
        put("155;48;255", "purple 1");
        put("145;44;238", "purple 2");
        put("125;38;205", "purple 3");
        put("85;26;139", "purple 4");
        put("216;191;216", "thistle");
        put("255;225;255", "thistle 1");
        put("238;210;238", "thistle 2");
        put("205;181;205", "thistle 3");
        put("139;123;139", "thistle 4");
        put("238;130;238", "violet");
        put("159;95;159", "violet blue");
        put("135;31;120", "Dark Purple");
        put("128;0;0", "Maroon");
        put("220;113;148", "Medium Violet Red");
        put("255;110;199", "Neon Pink");
        put("234;173;234", "Plum");
        put("217;192;217", "Thistle");
        put("173;234;234", "Turquoise");
        put("79;47;79", "Violet");
        put("204;50;153", "Violet Red");
        put("250;235;215", "Antique White");
        put("255;239;219", "Antique White 1");
        put("238;223;204", "Antique White 2");
        put("205;192;176", "Antique White 3");
        put("139;131;120", "Antique White 4");
        put("255;250;240", "Floral White");
        put("248;248;255", "Ghost White");
        put("255;222;173", "Navajo White");
        put("254;223;174", "Navajo White 1");
        put("238;207;161", "Navajo White 2");
        put("205;179;139", "Navajo White 3");
        put("139;121;94", "Navajo White 4");
        put("253;245;230", "Old Lace");
        put("246;246;246", "White Smoke");
        put("220;220;220", "gainsboro");
        put("255;255;240", "ivory");
        put("254;254;241", "ivory 1");
        put("238;238;224", "ivory 2");
        put("205;205;193", "ivory 3");
        put("139;139;131", "ivory 4");
        put("250;240;230", "linen");
        put("255;245;238", "seashell");
        put("254;246;239", "seashell 1");
        put("238;229;222", "seashell 2");
        put("205;197;191", "seashell 3");
        put("139;134;130", "seashell 4");
        put("255;250;250", "snow");
        put("254;251;251", "snow 1");
        put("238;233;233", "snow 2");
        put("205;201;201", "snow 3");
        put("139;137;137", "snow 4");
        put("245;222;179", "wheat");
        put("255;231;186", "wheat 1");
        put("238;216;174", "wheat 2");
        put("205;186;150", "wheat 3");
        put("139;126;102", "wheat 4");
        put("254;254;254", "white");
        put("217;217;243", "Quartz");
        put("216;216;191", "Wheat");
        put("255;235;205", "Blanched Almond");
        put("184;134;11", "Dark Goldenrod");
        put("255;185;15", "Dark Goldenrod 1");
        put("238;173;14", "Dark Goldenrod 2");
        put("205;149;12", "Dark Goldenrod 3");
        put("139;101;8", "Dark Goldenrod 4");
        put("255;250;205", "Lemon Chiffon");
        put("254;251;206", "Lemon Chiffon 1");
        put("238;233;191", "Lemon Chiffon 2");
        put("205;201;165", "Lemon Chiffon 3");
        put("139;137;112", "Lemon Chiffon 4");
        put("238;221;130", "Light Goldenrod");
        put("255;236;139", "Light Goldenrod 1");
        put("238;220;130", "Light Goldenrod 2");
        put("205;190;112", "Light Goldenrod 3");
        put("139;129;76", "Light Goldenrod 4");
        put("250;250;210", "Light Goldenrod Yellow");
        put("255;255;224", "Light Yellow");
        put("254;254;225", "Light Yellow 1");
        put("238;238;209", "Light Yellow 2");
        put("205;205;180", "Light Yellow 3");
        put("139;139;122", "Light Yellow 4");
        put("238;232;170", "Pale Goldenrod");
        put("255;239;213", "Papaya Whip");
        put("255;248;220", "corn silk");
        put("254;249;221", "corn silk 1");
        put("238;232;205", "corn silk 2");
        put("205;200;177", "corn silk 3");
        put("139;136;120", "corn silk 4");
        put("218;165;32", "goldenrod");
        put("255;193;37", "goldenrod 1");
        put("238;180;34", "goldenrod 2");
        put("205;155;29", "goldenrod 3");
        put("139;105;20", "goldenrod 4");
        put("255;228;181", "moccasin");
        put("255;255;0", "yellow");
        put("254;254;1", "yellow 1");
        put("238;238;0", "yellow 2");
        put("205;205;0", "yellow 3");
        put("139;139;0", "yellow 4");
        put("255;215;0", "gold");
        put("254;216;1", "gold 1");
        put("238;201;0", "gold 2");
        put("205;173;0", "gold 3");
        put("139;117;0", "gold 4");
        put("220;220;113", "Goldenrod");
        put("234;234;174", "Medium Goldenrod");
        put("153;204;50", "Yellow Green");
    }};
    private ImageView start;
    private ImageView stop;
    private DroidSpeech droidSpeech;
    SharedPreferences sharedPreferences;
    private SpeechRecognizer recognizer;
    public static Context contextOfApplication;
    Handler handler;

    /*[OPENCV]*************************************************************************************/
    static {
        if (!OpenCVLoader.initDebug()) {
            Log.e("OpenCVLoader.CA", "OpenCV Initialization failed.");
        } else {
            Log.e("OpenCVLoader.CA", "OpenCV Initialization success.");
        }
    }


    /*[DEFAULT TF]*********************************************************************************/
    @Override
    public void onPreviewSizeChosen(final Size size, final int rotation) {
        final float textSizePx =
                TypedValue.applyDimension(
                        TypedValue.COMPLEX_UNIT_DIP, TEXT_SIZE_DIP, getResources().getDisplayMetrics());
        borderedText = new BorderedText(textSizePx);
        borderedText.setTypeface(Typeface.MONOSPACE);

        tracker = new MultiBoxTracker(this);

        int cropSize = TF_OD_API_INPUT_SIZE;
        try {
            detector = TensorFlowObjectDetectionAPIModel.create(
                    getAssets(), TF_OD_API_MODEL_FILE, TF_OD_API_LABELS_FILE, TF_OD_API_INPUT_SIZE);
            cropSize = TF_OD_API_INPUT_SIZE;
        } catch (final IOException e) {
            LOGGER.e("Exception initializing classifier!", e);
            Toast toast =
                    Toast.makeText(
                            getApplicationContext(), "Classifier could not be initialized", Toast.LENGTH_SHORT);
            toast.show();
            finish();
        }

        previewWidth = size.getWidth();
        previewHeight = size.getHeight();

        sensorOrientation = rotation - getScreenOrientation();
        LOGGER.i("Camera orientation relative to screen canvas: %d", sensorOrientation);

        LOGGER.i("Initializing at size %dx%d", previewWidth, previewHeight);
        rgbFrameBitmap = Bitmap.createBitmap(previewWidth, previewHeight, Config.ARGB_8888);
        croppedBitmap = Bitmap.createBitmap(cropSize, cropSize, Config.ARGB_8888);

        frameToCropTransform =
                ImageUtils.getTransformationMatrix(
                        previewWidth, previewHeight,
                        cropSize, cropSize,
                        sensorOrientation, MAINTAIN_ASPECT);

        cropToFrameTransform = new Matrix();
        frameToCropTransform.invert(cropToFrameTransform);

        trackingOverlay = (OverlayView) findViewById(R.id.tracking_overlay);
        trackingOverlay.addCallback(
                new DrawCallback() {
                    @Override
                    public void drawCallback(final Canvas canvas) {
                        tracker.draw(canvas);
                        if (isDebug()) {
                            tracker.drawDebug(canvas);
                        }
                    }
                });

        addCallback(
                new DrawCallback() {
                    @Override
                    public void drawCallback(final Canvas canvas) {
                        if (!isDebug()) {
                            return;
                        }
                        final Bitmap copy = cropCopyBitmap;
                        if (copy == null) {
                            return;
                        }

                        final int backgroundColor = Color.argb(100, 0, 0, 0);
                        canvas.drawColor(backgroundColor);

                        final Matrix matrix = new Matrix();
                        final float scaleFactor = 2;
                        matrix.postScale(scaleFactor, scaleFactor);
                        matrix.postTranslate(
                                canvas.getWidth() - copy.getWidth() * scaleFactor,
                                canvas.getHeight() - copy.getHeight() * scaleFactor);
                        canvas.drawBitmap(copy, matrix, new Paint());

                        final Vector<String> lines = new Vector<String>();
                        if (detector != null) {
                            final String statString = detector.getStatString();
                            final String[] statLines = statString.split("\n");
                            for (final String line : statLines) {
                                lines.add(line);
                            }
                        }
                        lines.add("");

                        lines.add("Frame: " + previewWidth + "x" + previewHeight);
                        lines.add("Crop: " + copy.getWidth() + "x" + copy.getHeight());
                        lines.add("View: " + canvas.getWidth() + "x" + canvas.getHeight());
                        lines.add("Rotation: " + sensorOrientation);
                        lines.add("Inference time: " + lastProcessingTimeMs + "ms");

                        borderedText.drawLines(canvas, 10, canvas.getHeight() - 10, lines);
                    }
                });
    }

    @Override
    protected void processImage() {
        ++timestamp;
        final long currTimestamp = timestamp;
        byte[] originalLuminance = getLuminance();
        tracker.onFrame(
                previewWidth,
                previewHeight,
                getLuminanceStride(),
                sensorOrientation,
                originalLuminance,
                timestamp);
        trackingOverlay.postInvalidate();

        // No mutex needed as this method is not reentrant.
        if (computingDetection) {
            readyForNextImage();
            return;
        }
        computingDetection = true;
        LOGGER.i("Preparing image " + currTimestamp + " for detection in bg thread.");

        rgbFrameBitmap.setPixels(getRgbBytes(), 0, previewWidth, 0, 0, previewWidth, previewHeight);

        if (luminanceCopy == null) {
            luminanceCopy = new byte[originalLuminance.length];
        }
        System.arraycopy(originalLuminance, 0, luminanceCopy, 0, originalLuminance.length);
        readyForNextImage();

        final Canvas canvas = new Canvas(croppedBitmap);
        canvas.drawBitmap(rgbFrameBitmap, frameToCropTransform, null);

        // For examining the actual TF input.
        if (SAVE_PREVIEW_BITMAP) {
            ImageUtils.saveBitmap(croppedBitmap);
        }

        runInBackground(
                new Runnable() {
                    @Override
                    public void run() {
                        LOGGER.i("Running detection on image " + currTimestamp);
                        final long startTime = SystemClock.uptimeMillis();
                        final List<Classifier.Recognition> results = detector.recognizeImage(croppedBitmap);
                        lastProcessingTimeMs = SystemClock.uptimeMillis() - startTime;

                        cropCopyBitmap = Bitmap.createBitmap(croppedBitmap);
                        final Canvas canvas = new Canvas(cropCopyBitmap);
                        final Paint paint = new Paint();
                        paint.setColor(Color.RED);
                        paint.setStyle(Style.STROKE);
                        paint.setStrokeWidth(2.0f);

                        float minimumConfidence = MINIMUM_CONFIDENCE_TF_OD_API;
                        switch (MODE) {
                            case TF_OD_API:
                                minimumConfidence = MINIMUM_CONFIDENCE_TF_OD_API;
                                break;
                        }

                        final List<Classifier.Recognition> mappedRecognitions = new LinkedList<Classifier.Recognition>();
                        ArrayList<String> tempList = new ArrayList<String>();

                        for (final Classifier.Recognition result : results) {
                            final RectF location = result.getLocation();
                            if (location != null && result.getConfidence() >= minimumConfidence) {
                                canvas.drawRect(location, paint);

                                cropToFrameTransform.mapRect(location);
                                result.setLocation(location);
                                mappedRecognitions.add(result);

                                tempList.add(result.getTitle() + ";" + result.getConfidence().toString());
                            }
                        }
                        detectedObjects = tempList;
                        tracker.trackResults(mappedRecognitions, luminanceCopy, currTimestamp);
                        trackingOverlay.postInvalidate();
                        requestRender();
                        computingDetection = false;
//                        LOGGER.e("/////////////////////////: %s", Arrays.toString(detectedObjects.toArray()));
//                        LOGGER.e("Detect: %s", results);
                    }
                });
    }

    @Override
    protected int getLayoutId() {
        return R.layout.camera_connection_fragment_tracking;
    }

    @Override
    protected Size getDesiredPreviewFrameSize() {
        return DESIRED_PREVIEW_SIZE;
    }

    @Override
    public void onSetDebug(final boolean debug) {
        detector.enableStatLogging(debug);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        handler = new Handler();
        stop = findViewById(R.id.stop);
        start = findViewById(R.id.start);
        contextOfApplication = getApplicationContext();
        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        sayTTS("");

        if (sharedPreferences.getString("list_set_stt","").equals("2")) {
            runRecognizerSetup();
            runDSpeechSetup();
        } else if (sharedPreferences.getString("list_set_stt","").equals("1")) {
            runDSpeechSetup();
        } else {
            start.setEnabled(false);
            start.setVisibility(View.INVISIBLE);
            stop.setEnabled(false);
            stop.setVisibility(View.INVISIBLE);
        }
    }


    /*[DROID SPEECH]*******************************************************************************/
    public void runDSpeechSetup() {
        droidSpeech = new DroidSpeech(this, getFragmentManager());
        droidSpeech.setOnDroidSpeechListener(this);
        droidSpeech.setContinuousSpeechRecognition(false);
        droidSpeech.setOfflineSpeechRecognition(true);
        start.setEnabled(true);
        stop.setEnabled(true);
        start.setOnClickListener(this);
        stop.setOnClickListener(this);
    }

    @Override
    public void onDroidSpeechSupportedLanguages(String currentSpeechLanguage, List<String> supportedSpeechLanguages) {
        if (supportedSpeechLanguages.contains("en-US")) {
            // Setting the droid speech preferred language as tamil if found
            droidSpeech.setPreferredLanguage("en-US");
            // Setting the confirm and retry text in tamil
//            droidSpeech.setOneStepVerifyConfirmText("Confirm");
//            droidSpeech.setOneStepVerifyRetryText("Try Again");
        }
    }

    @Override
    public void onDroidSpeechRmsChanged(float rmsChangedValue) {
    }

    @Override
    public void onDroidSpeechLiveResult(String liveSpeechResult) {
    }

    @Override
    public void onDroidSpeechFinalResult(String finalSpeechResult) {
        stop.setVisibility(View.GONE);
        start.setVisibility(View.VISIBLE);

        String command = finalSpeechResult.toLowerCase();
        if (command.contains("what")) {
            if (command.contains("color")) {
                sendColor(getWindow().getDecorView().getRootView().findViewById(R.id.button1));
            } else if (command.contains("object")) {
                sendObject(getWindow().getDecorView().getRootView().findViewById(R.id.button2));
            }
        } else if (command.equals("exit") || command.equals("quit")) {
            // TODO: Say goodbye here or something to indicate it's closed
            sayTTS("good bye");
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    shutDown();
                }
            },500);
        }
    }

    @Override
    public void onDroidSpeechClosedByUser() {
        stop.setVisibility(View.GONE);
        start.setVisibility(View.VISIBLE);
    }

    @Override
    public void onDroidSpeechError(String errorMsg) {
        // Speech error
        Toast.makeText(this, errorMsg, Toast.LENGTH_LONG).show();
        stop.post(new Runnable() {
            @Override
            public void run() {
                // Stop listening
                stop.performClick();
            }
        });
    }

    @Override
    public void onDroidSpeechAudioPermissionStatus(boolean audioPermissionGiven, String errorMsgIfAny) {
        if (audioPermissionGiven) {
            start.post(new Runnable() {
                @Override
                public void run() {
                    // Start listening
                    start.performClick();
                }
            });
        } else {
            if (errorMsgIfAny != null) {
                // Permissions error
                Toast.makeText(this, errorMsgIfAny, Toast.LENGTH_LONG).show();
            }

            stop.post(new Runnable() {
                @Override
                public void run() {
                    // Stop listening
                    stop.performClick();
                }
            });
        }
    }

    @Override
    public synchronized void onPause() {
        super.onPause();
        if (stop.getVisibility() == View.VISIBLE) {
            stop.performClick();
        }
    }

    @Override
    public synchronized void onDestroy() {
        super.onDestroy();
//        droidSpeech.closeDroidSpeechOperations();
        if (stop.getVisibility() == View.VISIBLE) {
            stop.performClick();
        }
    }

    @Override
    public void onClick(View view) {

        if (!sharedPreferences.getString("list_set_stt","").equals("0")) {
            switch (view.getId()) {
                case R.id.start:
                    if (sharedPreferences.getString("list_set_stt","").equals("2")) {
                        recognizer.cancel();
                    }
                    // Starting droid speech
                    droidSpeech.startDroidSpeechRecognition();
                    // Setting the view visibilities when droid speech is running
                    start.setVisibility(View.GONE);
                    stop.setVisibility(View.VISIBLE);
                    handler.postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            droidSpeech.closeDroidSpeechOperations();
                            stop.setVisibility(View.GONE);
                            start.setVisibility(View.VISIBLE);
                            new Handler().postDelayed(new Runnable() {
                                @Override
                                public void run() {
                                    if (sharedPreferences.getString("list_set_stt","").equals("2")) {
                                        recognizer.startListening(KWS_SEARCH);
                                    }
                                }
                            },250);
                        }
                    }, 6000);
                    break;
                case R.id.stop:
                    // Closing droid speech
                    handler.removeCallbacksAndMessages(null);
                    droidSpeech.closeDroidSpeechOperations();
                    stop.setVisibility(View.GONE);
                    start.setVisibility(View.VISIBLE);
                    new Handler().postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            if (sharedPreferences.getString("list_set_stt","").equals("2")) {
                                recognizer.startListening(KWS_SEARCH);
                            }
                        }
                    },250);
                    break;
            }
        }
    }

    /*[POCKET SPHINX]******************************************************************************/
    private void runRecognizerSetup() {
        // Recognizer initialization is a time-consuming and it involves IO,
        // so we execute it in async task
        new AsyncTask<Void, Void, Exception>() {
            @Override
            protected Exception doInBackground(Void... params) {
                try {
                    Assets assets = new Assets(DetectorActivity.this);
                    File assetDir = assets.syncAssets();
                    SpeechRecognizerSetup speechRecognizerSetup = defaultSetup();
                    speechRecognizerSetup.setAcousticModel(new File(assetDir, "en-us-ptm"));
                    speechRecognizerSetup.setDictionary(new File(assetDir, "cmudict-en-us.dict"));
                    speechRecognizerSetup.setKeywordThreshold(1e-45f);
                    speechRecognizerSetup.setBoolean("-allphone_ci", true);

                    recognizer = speechRecognizerSetup.getRecognizer();
                    recognizer.addListener(new PocketSphinxRecognitionListener());
                    recognizer.addKeyphraseSearch(KWS_SEARCH, KEYPHRASE);
                } catch (IOException e) {
                    return e;
                }
                return null;
            }
            @Override
            protected void onPostExecute(Exception result) {
                if (result != null) {
                    Toast.makeText(getApplicationContext(), "Failed to init mPocketSphinxRecognizer ", Toast.LENGTH_SHORT).show();
                } else {
                    switchSearch(KWS_SEARCH);
                }
            }
        }.execute();
    }

    protected class PocketSphinxRecognitionListener implements RecognitionListener {

        @Override
        public void onPartialResult(Hypothesis hypothesis) {
//            Log.e("onPartialResult.DA", "HERE");
            if (hypothesis == null) {
                return;
            } else {
                String text = hypothesis.getHypstr();
                if (text.equals(KEYPHRASE)) {
                    recognizer.cancel();
                    start.performClick();
                }
            }
        }

        @Override
        public void onResult(Hypothesis hypothesis) {
        }

        @Override
        public void onBeginningOfSpeech() {
//            Log.e("onBeginningOfSpeech", "HERE");
        }

        @Override
        public void onEndOfSpeech() {
        }

        @Override
        public void onError(Exception error) {
            Log.e("onError.DA", error.getMessage());
        }

        @Override
        public void onTimeout() {
        }
    }

    @Override
    public void onStop() {;
        super.onStop();
        if (recognizer != null) {
            recognizer.cancel();
            recognizer.shutdown();
        }
    }

    private void switchSearch(String searchName) {
        recognizer.stop();
        if (searchName.equals(KWS_SEARCH)) {
            recognizer.startListening(searchName);
        }
    }

    /*[OTHER]**************************************************************************************/
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main_btn, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle item selection
        switch (item.getItemId()) {
            case R.id.menu_main:
                Intent intent_settings = new Intent(DetectorActivity.this, SettingsActivity.class);
                startActivity(intent_settings);
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    @Override
    public void onBackPressed() {
        if(isTaskRoot()) {
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setMessage("Are you sure you want to exit?")
                    .setCancelable(false)
                    .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int id) {
                            DetectorActivity.super.onBackPressed();
                        }
                    })
                    .setNegativeButton("No", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int id) {
                            dialog.cancel();
                        }
                    });
            AlertDialog alert = builder.create();
            alert.show();

        } else {
            super.onBackPressed();
        }
    }

    public static Context getContextOfApplication() {
        return contextOfApplication;
    }

    public void shutDown() {
        stopService(new Intent(DetectorActivity.this, ttsService.class));
        droidSpeech.closeDroidSpeechOperations();
        moveTaskToBack(true);
        android.os.Process.killProcess(android.os.Process.myPid());
        System.exit(1);
    }

    public void sayTTS(String string) {
        boolean tts_mode = sharedPreferences.getBoolean("switch_set_tts", false);
        if (tts_mode) {
            Intent i = new Intent(getApplicationContext(), ttsService.class);
            i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);  // TODO (cleanup): is this necessary?
            i.putExtra("key", string);
            startService(i);
        }
    }

    public void sendColor(View view) {

        rgbFrameBitmap.setPixels(getRgbBytes(), 0, previewWidth, 0, 0, previewWidth, previewHeight);
        boolean advanced_mode = sharedPreferences.getBoolean("switch_set_cols", false);
        boolean filtering_mode = sharedPreferences.getBoolean("switch_set_filt", false);
        int size = Integer.parseInt(sharedPreferences.getString("text_ROIsize", "50"));
        int color_index = 0;
        int frame_w = rgbFrameBitmap.getWidth();
        int frame_h = rgbFrameBitmap.getHeight();
        /*
        * FRAME (DetectorActivity) -> CANVAS (MultiBoxTracker)
        * height_p2 = h + size     -> w_centred - offsetSize [left]
        * height_p1 = h - size     -> w_centred + offsetSize [right]
        * width_p2  = w + size     -> h_centred + offsetSize [bottom]
        * width_p1  = w - size     -> h_centred - offsetSize [top]
        */
        int height_p1 = (frame_h / 2) - size;
        int width_p1 = (frame_w / 2) - size;
        int height_p2 = (frame_h / 2) + size;
        int width_p2 = (frame_w / 2) + size;
        double r_avg;
        double b_avg;
        double g_avg;
        double dif_val;
        String closest_color;
        double r_sum = 0;
        double g_sum = 0;
        double b_sum = 0;
        double min_dif = 16581375;
        Mat frame_clone = new Mat();

        Utils.bitmapToMat(rgbFrameBitmap, frame_clone);
        if (filtering_mode) {
            Imgproc.GaussianBlur(frame_clone, frame_clone, new org.opencv.core.Size(5, 5), 1, 1);
        }
        for (int x = width_p1; x <= width_p2; x++) {
            for (int y = height_p1; y <= height_p2; y++) {
                double[] rgb = frame_clone.get(y, x);
                r_sum += rgb[0];
                g_sum += rgb[1];
                b_sum += rgb[2];
            }
        }
        r_avg = r_sum / ((size * 2) * (size * 2));
        g_avg = g_sum / ((size * 2) * (size * 2));
        b_avg = b_sum / ((size * 2) * (size * 2));
        for (int i = 0; i < cols_dict.size(); i++) {
            String[] par_col = cols_dict.keySet().toArray()[i].toString().split(";");
            dif_val = ((Integer.parseInt(par_col[0]) - r_avg) * (Integer.parseInt(par_col[0]) - r_avg) +
                    ((Integer.parseInt(par_col[1]) - g_avg) * (Integer.parseInt(par_col[1]) - g_avg)) +
                    ((Integer.parseInt(par_col[2]) - b_avg) * (Integer.parseInt(par_col[2]) - b_avg)));
            if (min_dif > dif_val) {
                min_dif = dif_val;
                color_index = i;
            }
        }
        if (advanced_mode) {
            closest_color = cols_dict.get(cols_dict.keySet().toArray()[color_index].toString());
        } else {
            if (color_index >= 0 && color_index <= 9) {
                closest_color = "grey";
            } else if (color_index >= 10 && color_index <= 51) {
                closest_color = "black";
            } else if (color_index >= 52 && color_index <= 83) {
                closest_color = "grey";
            } else if (color_index >= 84 && color_index <= 115) {
                closest_color = "white";
            } else if (color_index >= 116 && color_index <= 239) {
                closest_color = "blue";
            } else if (color_index >= 240 && color_index <= 280) {
                closest_color = "brown";
            } else if (color_index >= 281 && color_index <= 350) {
                closest_color = "green";
            } else if (color_index >= 351 && color_index <= 401) {
                closest_color = "orange";
            } else if (color_index >= 402 && color_index <= 473) {
                closest_color = "red";
            } else if (color_index >= 474 && color_index <= 541) {
                closest_color = "violet";
            } else if (color_index >= 542 && color_index <= 580) {
                closest_color = "white";
            } else if (color_index >= 581 && color_index <= 628) {
                closest_color = "yellow";
            } else {  // Should never occur. . .
                closest_color = "error";
            }
        }
        Toast.makeText(getApplicationContext(), closest_color, Toast.LENGTH_LONG).show();
        sayTTS(closest_color);
    }

    public void sendObject(View view) {
        //TODO (list):
        //1 - Add support for calling the object closest to the center of the screen instead of highest confidence
        //2 - Fix trouble getting multiple objects (simplify interface between methods?)

        boolean advanced_mode = sharedPreferences.getBoolean("switch_set_confstr", false);
        String sentence = "";
        String objectName = "";
        String objectConfidence;
        String objectList = Arrays.toString(detectedObjects.toArray());

        if (!objectList.equals("[]")) {
            objectList = objectList.replace("[", "").replace("]", "");
            String[] objects = objectList.split(",");

            int numObjects = objects.length;
            objectName = objects[0].split(";")[0];
            objectConfidence = String.format(java.util.Locale.US, "%.1f", Float.parseFloat(objects[0].split(";")[1]) * 100) + "% ";

            // TODO (fix [LOW]): find an elegant fix for "bad" labels in 'coco_label_list.txt'
            if (objectName.equals("tv")) {
                objectName = "t.v.";
            }

            if (advanced_mode) {
                sentence = "I am " + objectConfidence + "confident that the object is ";
            } else {
                sentence = "The object is ";
            }
            if ("AEIOUaeiou".indexOf(objectName.charAt(0)) != -1) {
                sentence += "an " + objectName;
            } else {
                sentence += "a " + objectName;
            }
            Toast.makeText(getApplicationContext(), sentence, Toast.LENGTH_LONG).show();
        }
        sayTTS(sentence);
    }
}
