## Amazon Alexa skill template

Created 6/29/2022

### Instructions to add a skill:
  1. In the Amazon Alexa Developer Console, click on **Create a Skill**. 
  ![image](https://user-images.githubusercontent.com/41808114/176571291-fefa3d30-76eb-40ec-94e0-899dda9da65c.png)
  3. Enter the skill name. This can not be changed after it has been created.
    <br/>a. For the first field, choose **custom model**.
    <br/>b. For the second field, choose **Alexa-hosted (Python)** since we are using Python as the language.
    <br/>c. When finished, select **Create The Skill** on the top right corner of the page.
  ![image](https://user-images.githubusercontent.com/41808114/176571974-d21d7a2e-e231-48d9-9455-b810932e1700.png)
  3. Select **Import Skill**. Use the GitHub repository link and select **import**.
  ![image](https://user-images.githubusercontent.com/41808114/176571868-fb9051da-ed1e-4ab8-9749-657030070364.png)
  4. Once the skill has been created, we need to change the skill invocation name. Make sure you are on **Build** tab at the top of the page. On the side panel, navigate to **Invocations -> Skill Invocation Name** and modify the invocation name. This will be used to trigger the launch of the skill. When finished, click on **Build Model** at the top of the page.
  ![image](https://user-images.githubusercontent.com/41808114/176572245-f45a57c7-e2b5-4ceb-b538-6865a4e93ce6.png)
  5. On the side panel, navigate to **Interaction Model -> Intents -> PlayRadioStationIntent**. Delete the existing sample utterances related to the template (Smooth Jazz Radio). Add sample utterances that are related to your Alexa Skill. Click on **Build Model** when finished.
![image](https://user-images.githubusercontent.com/41808114/176573021-352173c3-8391-474e-a53e-fbcab890c210.png)
  6. Navigate to **Code** Tab. On the side panel, open the **lambda_function.py** if it isn't open already. Here is the main logic for the Alexa Skill, and the URL for the station is held in here.
    <br/>a. Under **STREAMS**, modify the **["url"]** to the radio station URL. **THE URL MUST BE HTTPS AND HAVE A VALID SSL CERTIFICATE**.
    <br/>b. If applicable, modify the **["metadata"]["subtitle"]** field. This is displayed on devices with a screen.
    <br/>c. Under **["metadata"]["title"]** modify the title of the radio station. This is said out loud to the user before the radio station starts playing.
    <br/>d. Under **["art"]["sources"]** modify the content description and the image url for the radio station. This will be displayed on certain Alexa devices that have a display (Amazon Echo Show).
    ![image](https://user-images.githubusercontent.com/41808114/176575007-00c977f8-65a1-49cf-8cf7-50d5342a6d28.png)
  7. If necessary, modify the strings for the reponses.
  ![image](https://user-images.githubusercontent.com/41808114/176575275-edad3591-b458-4c8e-af55-b0a53e8c75e4.png)
  8. When finished, click **Deploy** at the top of the page.
  ![image](https://user-images.githubusercontent.com/41808114/176580377-75141427-22aa-474b-8d9b-1d0680a40cbe.png)
  9. Navigate to the **Test** tab at the top of the page. Enable the skill testing by selecting **Development**. Here you can test the skill in the simulator, or through your Alexa enabled device by using the phrase _"Alexa, play {skill invocation name}."_
  ![image](https://user-images.githubusercontent.com/41808114/176577008-c315cd5b-f1a0-4416-937f-dc69fc864bd8.png)
  10. To deploy, use the **Distribution** tab. 
