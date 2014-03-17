---
layout: post
title: "Custom Layout Interactions on Android for Fun And Profit"
date: 2014-03-16 15:00:00
tags: android design
excerpt: The Android Market, erm Play Store, has finally become crowded enough for developers to pay attention to their application's design in an attempt to woo users away from their competitors, and honestly I couldn't be happier. Just a few short years ago no one even gave Android design a second though, and we still see Gingerbread's orange glow shining through today. Last week I attended an Android Design Meetup and the enthusiasm in the room was palatable.
---

The Android Market, erm Play Store, has finally become crowded enough for developers to pay attention to their application's design in an attempt to woo users away from their competitors, and honestly I couldn't be happier. Just a few short years ago no one even gave Android design a second though, and we still see Gingerbread's orange glow shining through today. Last week I attended an [Android Design Meetup](http://www.meetup.com/android-developers-nyc/events/169173012) and the enthusiasm in the room was palatable. The presenters [shared](https://speakerdeck.com/kevingrant/android-design-beyond-the-guidelines-short-version) [some great](https://speakerdeck.com/kevingrant/android-design-beyond-the-guidelines-short-version) [tips](http://www.slideshare.net/denizmveli/etsy-androiddesigntalk) that I highly recommend everyone checkout. Having recently made the realization that quality is king myself, I've been playing with different ways of improving the experience in my application [onTour](https://play.google.com/store/apps/details?id=collegelabs.onTour.free&referrer=utm_source%3Dblog%26utm_medium%3Dcustom-layouts-for-fun-and-profit) and figured I might as well share some of them.

## Demo

<div class="center-text">
<video width="270" height="480" autoplay="autoplay" loop="loop" controls="controls">
  <source src="/assets/videos/events_scrolling.mp4" type="video/mp4" />
  Your browser does not support the video tag.
</video>
</div>

Isn't that nice? Personally I find it a lot more enjoyable than just having the image scroll off the page. So how can you accomplish this effect? Lets dive into it.


For this effect to be complete, we need the following:
- Graphic content to scroll up but underneath the scrollable content
- A transparent sticky header that slides over the graphic like a colored piece of glass
- The image to scroll at half speed, so it stops scrolling when its center is at the top

The Layout for this view is something like this

{% highlight java %}

<?xml version="1.0" encoding="utf-8"?>
<collegelabs.onTour.library.views.ObservableScrollView
        xmlns:android="http://schemas.android.com/apk/res/android"
        android:id="@+id/scroll_view"
        android:layout_width="match_parent"
        android:layout_height="match_parent">

<FrameLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent">

    <LinearLayout android:layout_width="match_parent"
                  android:layout_height="wrap_content"
                  android:orientation="vertical"
            >

        <FrameLayout
                android:id="@+id/img_placeholder"
                android:layout_width="match_parent"
                android:layout_height="@dimen/event_img_height"
                />

        <LinearLayout
                android:id="@+id/scrollable_content"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                >
                <!-- Real content here -->
        </LinearLayout>

    </LinearLayout>

    <!-- The Banner Image to Scroll  -->
    <ImageView
            android:id="@+id/img_artist1"
            android:layout_width="match_parent"
            android:layout_height="@dimen/event_img_height"
            />

    <!-- The scrolling text view -->
    <TextView
                android:id="@+id/section_event_sticky"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:background="#99000000"
                android:gravity="center_vertical"
                />

    </FrameLayout>

</collegelabs.onTour.library.views.ObservableScrollView>

{% endhighlight %}


We've got a ScrollView that is holding our real content (the Event details), a placeholder view for the Image that will be moving and a TextView for the sticky header. The little magic that exists here is inside ObservableScrollView which allows us to hook into ScrollView's scroll events.


{% highlight java %}
/**
 * A custom ScrollView that can accept a scroll listener.
 */
public class ObservableScrollView extends ScrollView {
    private Callbacks mCallbacks;

    public ObservableScrollView(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    protected void onScrollChanged(int l, int t, int oldl, int oldt) {
        super.onScrollChanged(l, t, oldl, oldt);
        if (mCallbacks != null) {
            mCallbacks.onScrollChanged(t);
        }
    }

    public void setCallbacks(Callbacks listener) {
        mCallbacks = listener;
    }

    public static interface Callbacks {
        public void onScrollChanged(int scrollY);
    }
}

{% endhighlight %}



Then our Activity/Fragment can listen to scroll changes and adjust the Views positions as necessary.

{% highlight java %}

    public View onCreateView(LayoutInflater inflater,
        ViewGroup container, Bundle savedInstanceState) {
       
        // Get views by ids

        scrollView.setCallbacks(this);
        scrollView.getViewTreeObserver().addOnGlobalLayoutListener(
                new ViewTreeObserver.OnGlobalLayoutListener() {
                    @Override
                    public void onGlobalLayout() {
                        onScrollChanged(scrollView.getScrollY());
                    }
                });

         return scrollView;
     }


    @Override
    public void onScrollChanged(int scrollY) {
        int contentTop = scrollableContent.getTop();
        int stickyH = eventTitleSticky.getHeight();
        int placeholderLoc = contentTop - stickyH;

        int offset = artistImagePlaceholder.getTop();

        int imgH = artistImageBanner.getHeight();
        int imgW = artistImageBanner.getWidth();

        if(placeholderLoc > scrollY) {
            // Sticky header is below the top
            // keep it aligned with the placeholder
            ViewHelper.setTranslationY(eventTitleSticky, placeholderLoc);

            // Adjust the image position
            double distance = scrollY - contentTop;
            float transY = (float) 
                (distance / 2.0 + imgH / 2.0) - offset;
            ViewHelper.setTranslationY(artistImageBanner, transY);

            // Clip visible region of the image so the content 
            // is shown underneath as we scroll up
            Rect clipBounds = new Rect(0, 0, 
                imgW, (int) (imgH - transY));
            artistImageBanner.setClipableBounds(clipBounds);
        }else{
            // Sticky header is now stuck to the top
            ViewHelper.setTranslationY(eventTitleSticky, scrollY);

            // Adjust the image position
            float translationY = (scrollY - (imgH / 2.0f))
                 + (stickyH / 2.0f);
            ViewHelper.setTranslationY(artistImageBanner, translationY);
            
            // Clip visible region of the image so the content is shown
            // underneath as we scroll up
            Rect clipBounds = new Rect(0, 0, 
                imgW, (int) (imgH / 2.0 + stickyH / 2.0));
            artistImageBanner.setClipableBounds(clipBounds);
        }
    }

{% endhighlight %}

For those wondering, 
{% highlight java %}
ViewHelper.setTranslationY(view, dist);
{% endhighlight %}
is the [NineOldAndroids](https://github.com/JakeWharton/NineOldAndroids/)  equivalent of 
{% highlight java %}
view.setTranslationY(dist);
{% endhighlight %}
so this technique works all the way back to Froyo! (maybe beyond, but I haven't tested)

Hopefully thats enough to get on your way making beautiful Android apps, many thanks to Roman Nurik for the [basis](https://plus.google.com/+RomanNurik/posts/1Sb549FvpJt) of this technique and the Spotify + Airbnb apps for inspiration.

