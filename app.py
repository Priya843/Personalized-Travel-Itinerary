import streamlit as st
import openai

# Get the API key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state for input persistence
if "refine_details" not in st.session_state:
    st.session_state["refine_details"] = False
if "inputs" not in st.session_state:
    st.session_state["inputs"] = {}

# App title
st.title("AI Travel Planner")

# Step 1: Collect Basic User Input
if not st.session_state["refine_details"]:
    st.header("Plan Your Perfect Trip")
    destination = st.text_input("🌍 **Where are you planning to go?**", placeholder="e.g., Japan")
    duration = st.number_input("📅 **How many days will your trip be?**", min_value=1, max_value=30, step=1)
    budget = st.selectbox("💰 **What’s your budget?**", ["Low", "Moderate", "Luxury"])
    purpose = st.text_input("🎯 **What’s the purpose of your trip?**", placeholder="e.g., relaxation, adventure, cultural exploration")
    preferences = st.text_area("✨ **Any specific preferences?**", placeholder="e.g., food, attractions, mobility needs")

    # Save inputs to session state
    if st.button("🔍 Refine Details"):
        if not destination or not duration or not budget:
            st.warning("⚠️ Please provide all mandatory details!")
        else:
            st.session_state["inputs"] = {
                "destination": destination,
                "duration": duration,
                "budget": budget,
                "purpose": purpose,
                "preferences": preferences,
            }
            st.session_state["refine_details"] = True  # Transition to refinement

# Step 2: Refine Inputs
if st.session_state["refine_details"]:
    st.header("🔧 Refine Your Trip Details")
    inputs = st.session_state["inputs"]

    st.write(f"**🌍 Destination:** {inputs['destination']}")
    st.write(f"**📅 Duration:** {inputs['duration']} days")
    st.write(f"**💰 Budget:** {inputs['budget']}")
    st.write(f"**🎯 Purpose:** {inputs['purpose']}")
    st.write(f"**✨ Preferences:** {inputs['preferences']}")

    # Refinement inputs
    cities = st.text_input("🏙️ **Do you have specific cities in mind?**", placeholder="e.g., Mumbai, Delhi")
    dietary_restrictions = st.text_input("🍽️ **Any dietary preferences or restrictions?**", placeholder="e.g., vegetarian, vegan, none")
    mobility_concerns = st.selectbox("🚶 **Do you have mobility concerns?**", ["No", "Yes, limited walking", "Yes, wheelchair access needed"])
    accommodation = st.selectbox("🏨 **Accommodation preference?**", ["Luxury", "Budget", "Central location"])

    # Save refinement inputs to session state
    if st.button("🗺️ Generate Itinerary"):
        st.session_state["inputs"].update({
            "cities": cities,
            "dietary_restrictions": dietary_restrictions,
            "mobility_concerns": mobility_concerns,
            "accommodation": accommodation,
        })

        # Call the AI model to generate the itinerary
        with st.spinner("⏳ Generating your personalized itinerary..."):
            try:
                prompt = f"""
                You are an expert travel planning assistant dedicated to creating highly personalized, detailed, and realistic travel itineraries. Your goal is to generate a comprehensive {inputs['duration']}-day itinerary for a user based on their provided preferences and inputs. Ensure the itinerary is practical, engaging, and requires minimal additional research from the user.

                **User Details:**
                - **Destination:** {inputs['destination']}
                - **Duration:** {inputs['duration']} days
                - **Budget:** {inputs['budget']}
                - **Purpose:** {inputs['purpose']}
                - **Preferences:** {inputs['preferences']}
                - **Specific Cities:** {cities}
                - **Dietary Restrictions:** {dietary_restrictions}
                - **Mobility Concerns:** {mobility_concerns}
                - **Accommodation Preference:** {accommodation}

                **Output Requirements:**

                1. **Accommodation Details:**
                   - **Daily Accommodation:** For each day, recommend a specific hotel, hostel, or Airbnb where the user will be staying.
                     - **Name:** Provide the name of the accommodation.
                     - **Location:** Specify the area or neighborhood.
                     - **Price Range:** Indicate the nightly cost based on the user's budget.
                     - **Key Amenities:** Highlight essential amenities (e.g., free Wi-Fi, breakfast included, swimming pool).
                     - **Suitability:** Explain why this accommodation is ideal (e.g., proximity to attractions, family-friendly, luxury features).

                2. **Day-by-Day Itinerary:**
                   - **Structure:** Present a clear, organized day-by-day plan covering all {inputs['duration']} days.
                   - **Each Day Should Include:**
                     - **Check-In/Check-Out:**
                       - **Morning:** "Check-in at [Hotel Name]."
                       - **Evening (if applicable):** "Check-out from [Hotel Name]."
                     - **Activities:** Include **2-3 well-planned activities** per day to ensure a relaxed and enjoyable experience.
                       - **Morning Activity:**
                         - **Time:** e.g., "9:00 AM"
                         - **Activity:** e.g., "Breakfast at [Cafe Name], renowned for its [signature dish]."
                         - **Description:** Briefly explain what the user will experience.
                       - **Afternoon Activity:**
                         - **Time:** e.g., "1:00 PM"
                         - **Activity:** e.g., "Visit [Attraction Name], a must-see landmark because [reason]."
                         - **Description:** Provide insightful details about the activity.
                       - **Evening Activity:**
                         - **Time:** e.g., "6:00 PM"
                         - **Activity:** e.g., "Dinner at [Restaurant Name], offering [cuisine type] suitable for [dietary restriction]."
                         - **Description:** Highlight why this place is special.
                     - **Transportation:** Briefly explain how to travel between activities (e.g., walking, public transit, taxi).
                     - **Relaxation/Free Time:** Suggest a time slot for relaxation or spontaneous activities (e.g., "7:00 PM - Free time to explore local shops or relax at the hotel.")

                3. **Additional Recommendations:**
                   - **Food & Dining:**
                     - Recommend restaurants, cafes, or street food that align with the user's dietary preferences and budget.
                     - Mention signature dishes or must-try cuisines at each location.
                   - **Local Tips:**
                     - Provide cultural etiquette tips, safety advice, and useful local phrases.
                     - Include information about ticket bookings, expected crowds, or weather forecasts.
                   - **Personalization:**
                     - Highlight any special events, festivals, or seasonal activities occurring during the user's visit.
                     - Suggest personalized experiences based on user preferences (e.g., "Since you enjoy art, consider visiting the [Local Art Gallery] on Day 3.")

                **Tone:**
                - Maintain a **friendly, engaging, and conversational** tone throughout the itinerary.
                - Ensure the language is **clear and accessible**, making the user feel excited and confident about their trip.

                **Example Structure:**

                ---

                **Day 1: Arrival and Exploration**

                - **Check-In:** *Hotel Sunshine*, located in the heart of {inputs['destination']}. This [luxury/budget] hotel offers [free Wi-Fi, complimentary breakfast] and is just a short walk from [major attraction].

                - **9:00 AM - Breakfast at *Cafe Delight***: Start your day with a hearty breakfast featuring their famous [signature dish], perfect for fueling up.

                - **11:00 AM - Visit *[Attraction Name]***: Explore this iconic landmark known for [unique feature]. It's a great spot for photos and learning about the local culture.

                - **1:00 PM - Lunch at *[Restaurant Name]***: Enjoy delicious [cuisine type] that caters to your [dietary restrictions], offering dishes like [specific dish].

                - **3:00 PM - Free Time/Relaxation:** Take a leisurely stroll through [park/garden] or relax at your hotel.

                - **6:30 PM - Dinner at *[Restaurant Name]***: Experience [cuisine type] with a cozy ambiance, perfect for unwinding after a day of exploration.

                - **Transportation Tips:** Easily navigate using [public transit options] or enjoy a scenic walk to nearby attractions.

                - **Local Tip:** Remember to [cultural tip or safety advice].

                ---

                *Continue similarly for Days 2 to {inputs['duration']}.*

                ---
                """

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Ensure you have access to GPT-4 for better performance
                    messages=[
                        {"role": "system", "content": "You are an expert and friendly travel planner."},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=3000,  # Increased token limit to accommodate detailed output
                    temperature=0.7,
                )
                itinerary = response.choices[0].message.content
                st.success("🎉 **Here’s your personalized itinerary:**")
                st.markdown(itinerary)
            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")

# Footer
st.write("---")
st.write("Built with ❤️ using Streamlit and OpenAI.")

