---
layout: post
title: Custom Layout Animations For Fun And Profit
date:   2014-03-16 15:00:00
--

The Android Market, erm Play Store, has finally become crowded enough for developers to pay attention to their application's design in an attempt to woo users away from their competitors, and honestly I couldn't be happier. Just a few short years ago no one even gave Android design a second though, and we still see Gingerbread's orange glow shining through today. Last week I attended an [Android Design Meetup](http://www.meetup.com/android-developers-nyc/events/169173012) and the enthusiasm in the room was palatable. The presenters [shared](https://speakerdeck.com/kevingrant/android-design-beyond-the-guidelines-short-version) [some great](https://speakerdeck.com/kevingrant/android-design-beyond-the-guidelines-short-version) [tips](http://www.slideshare.net/denizmveli/etsy-androiddesigntalk) that I highly recommend everyone checkout. Having made the realization that quality is king myself, I've been on a binge of sorts to improve the experience in my application [onTour](https://play.google.com/store/apps/details?id=collegelabs.onTour.free&referrer=utm_source%3Dblog%26utm_medium%3Dcustom-layouts-for-fun-and-profit) and figured I might as well share some of them.

## Sliding panes demo
#TODO GIF


Isn't that nice? Personally I find it a lot more enjoyable than just having the image scroll off the page. So how can you accomplish this effect? Lets dive into it.


For this effect to be complete, we need the following:
- A transparent sticky header
- Graphic content to scroll up + under the header
- To keep the content centered as it scrolls (watch it again incase you didn't notice)

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

		<!-- background color necessary for the  to overdraw the image-->
        <LinearLayout
                android:id="@+id/scrollable_content"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:background="#F7F7F7"
                >
       			<!-- The views real content -->
       	</LinearLayout>

   	</LinearLayout>


 	<ImageView
            android:id="@+id/img_artist1"
            android:layout_width="match_parent"
            android:layout_height="@dimen/event_img_height"
            />

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

	@Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
    	scrollView = (ObservableScrollView) inflater.inflate(R.layout.event_details_header, container, false);

 		artistImageBanner = (AsyncImageView) scrollView.findViewById(R.id.img_artist1);
        artistImagePlaceholder = scrollView.findViewById(R.id.img_placeholder);
        eventTitleSticky = (TextView) scrollView.findViewById(R.id.section_event_sticky);
        scrollableContent = (LinearLayout) scrollView.findViewById(R.id.scrollable_content);
        artistContainer = (LinearLayout) scrollView.findViewById(R.id.section_event_artist_container);
       

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
        int scrollableContentTop = scrollableContent.getTop();
        int eventTitleStickyHeight = eventTitleSticky.getHeight();
        int placeholderLoc = scrollableContentTop - eventTitleStickyHeight;

        int offset = artistImagePlaceholder.getTop();

        int artistImageBannerHeight = artistImageBanner.getHeight();
        int artistImageBannerWidth = artistImageBanner.getWidth();

        if(placeholderLoc > scrollY) {
            ViewHelper.setTranslationY(eventTitleSticky, placeholderLoc);

            double distance = scrollY - scrollableContentTop;
            float transY = (float) (distance/2.0 + artistImageBannerHeight / 2.0) - offset;
            ViewHelper.setTranslationY(artistImageBanner, transY);

            artistImageBanner.setClipableBounds(new Rect(0,0,artistImageBannerWidth, (int) (artistImageBannerHeight - transY)));
        }else{
            float translationY = (scrollY - (artistImageBannerHeight / 2.0f)) + (eventTitleStickyHeight / 2.0f);
            ViewHelper.setTranslationY(artistImageBanner, translationY);
            artistImageBanner.setClipableBounds(new Rect(0, 0,artistImageBannerWidth, (int) (artistImageBannerHeight/2.0 + eventTitleStickyHeight/2.0)));
            ViewHelper.setTranslationY(eventTitleSticky, scrollY);
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




