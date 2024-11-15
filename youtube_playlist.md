This guide will help you set up an automated process to catalog YouTube playlist and video data into Port.

Using Port's GitHub action, you’ll fetch YouTube data and ingest it into Port for easy tracking and visualization.

  
## Prerequisites

1. [Create a Port account](https://app.getport.io) and set up API credentials.
2. [Obtain a YouTube Data API Key](https://console.cloud.google.com/apis/credentials).
3. [Set up GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) in your repository for:

-  `YOUTUBE_API_KEY`: Your YouTube API key.
-  `CLIENT_ID`: Your Port client ID.
-  `CLIENT_SECRET`: Your Port client secret.

  
## Step 1: Model Data in Port

Data modeling in Port involves defining entities and their relationships to ensure consistent, structured data. 

This step is crucial as it allows your system to understand and manage data efficiently, ensuring that different entities (like playlists and videos) interact seamlessly within workflows.

### Data model setup
1. Navigate to your [Port Builder](https://app.getport.io/settings/data-model) page.
2. Click the `+ Blueprint` button to create a new blueprint.
3. Click the Edit JSON button on the Modal


### Add Deployment blueprints.

Adding blueprints in Port helps define the structure and relationships of your data entities. 

For example, by adding the YouTube playlist and Youtube video blueprints, you can ensure that the necessary properties for each blueprint (like title, description, and link) are captured and organized consistently within the system. This enables better data management and interaction with APIs.

<details>
<summary>Youtube playlist blueprint (click to expand)</summary>

```json showLineNumbers
{
  "identifier": "youtube_playlist",
  "title": "YouTube Playlist",
  "icon": "YouTube",
  "schema": {
    "properties": {
      "link": {
        "type": "string",
        "title": "Playlist Link",
        "format": "url",
        "description": "The URL link to the YouTube playlist."
      },
      "playlistDescription": {
        "type": "string",
        "title": "Playlist Description",
        "description": "A detailed description of the YouTube playlist."
      },
      "publishedAt": {
        "type": "string",
        "title": "Publish Date",
        "format": "date-time",
        "description": "The date and time when the playlist was published."
      },
      "channelId": {
        "type": "string",
        "title": "Channel ID",
        "description": "The ID of the YouTube channel that owns the playlist."
      },
      "channelTitle": {
        "type": "string",
        "title": "Channel Title",
        "description": "The title of the YouTube channel that owns the playlist."
      },
      "thumbnails": {
        "type": "object",
        "title": "Thumbnails",
        "description": "Various resolution thumbnails for the playlist.",
        "properties": {
          "default": {
            "type": "string",
            "title": "Default Thumbnail",
            "description": "URL for the default thumbnail image."
          },
          "medium": {
            "type": "string",
            "title": "Medium Thumbnail",
            "description": "URL for the medium-sized thumbnail image."
          },
          "high": {
            "type": "string",
            "title": "High Thumbnail",
            "description": "URL for the high-resolution thumbnail image."
          },
          "standard": {
            "type": "string",
            "title": "Standard Thumbnail",
            "description": "URL for the standard thumbnail image."
          }
        }
      },
      "localized": {
        "type": "object",
        "title": "Localized Information",
        "description": "Localized title and description for different regions.",
        "properties": {
          "title": {
            "type": "string",
            "title": "Localized Title",
            "description": "The localized title of the playlist."
          },
          "description": {
            "type": "string",
            "title": "Localized Description",
            "description": "The localized description of the playlist."
          }
        }
      }
    },
    "required": [
      "playlistDescription",
      "publishedAt",
      "channelId",
      "channelTitle"
    ]
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {}
}
```

</details>

<details>
<summary>Youtube video blueprint (click to expand)</summary>

```json showLineNumbers
{
  "identifier": "youtube_video",
  "title": "YouTube Video",
  "icon": "YouTube",
  "schema": {
    "properties": {
      "link": {
        "type": "string",
        "title": "Video Link",
        "format": "url",
        "description": "The URL link to the YouTube video."
      },
      "duration": {
        "type": "string",
        "title": "Video Duration",
        "description": "The duration of the YouTube video."
      },
      "videoDescription": {
        "type": "string",
        "title": "Video Description",
        "description": "A detailed description of the YouTube video."
      },
      "publishedAt": {
        "type": "string",
        "title": "Publish Date",
        "format": "date-time",
        "description": "The date and time when the video was published."
      },
      "position": {
        "type": "number",
        "title": "Position in Playlist",
        "description": "The video's position in the playlist."
      },
      "likes": {
        "type": "number",
        "title": "Like Count",
        "description": "The number of likes on the video."
      },
      "views": {
        "type": "number",
        "title": "View Count",
        "description": "The number of views on the video."
      },
      "comments": {
        "type": "number",
        "title": "Comment Count",
        "description": "The number of comments on the video."
      },
      "thumbnails": {
        "type": "object",
        "title": "Thumbnails",
        "description": "Various resolution thumbnails for the video.",
        "properties": {
          "default": {
            "type": "string",
            "title": "Default Thumbnail",
            "description": "URL for the default thumbnail image."
          },
          "medium": {
            "type": "string",
            "title": "Medium Thumbnail",
            "description": "URL for the medium-sized thumbnail image."
          },
          "high": {
            "type": "string",
            "title": "High Thumbnail",
            "description": "URL for the high-resolution thumbnail image."
          },
          "standard": {
            "type": "string",
            "title": "Standard Thumbnail",
            "description": "URL for the standard thumbnail image."
          },
          "maxres": {
            "type": "string",
            "title": "Max Resolution Thumbnail",
            "description": "URL for the maximum resolution thumbnail image."
          }
        }
      },
      "videoOwnerChannelTitle": {
        "type": "string",
        "title": "Channel Title",
        "description": "The title of the channel that owns the video."
      },
      "videoOwnerChannelId": {
        "type": "string",
        "title": "Channel ID",
        "description": "The ID of the channel that owns the video."
      }
    },
    "required": [
      "videoDescription",
      "publishedAt",
      "duration",
      "link"
    ]
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {
    "playlist": {
      "title": "Playlist",
      "many": false,
      "target": "youtube_playlist",
      "required": true
    }
  }
}

```

<center>
	<img  src='/img/data_model_blueprints.png'  border='1px'  />
</center>

</details>

  
## Step 2: GitHub Workflow for Data Ingestion

A GitHub workflow for data ingestion automates the process of pulling data from external sources (like YouTube) and processing it for use within your application. 

By defining this workflow, you ensure that the data ingestion process is consistent, automated, and integrated into your development pipeline. This helps in efficiently handling data updates and maintaining data quality.

### Create a Youtube Catalog Blueprint using JSON definition.

<details>

<summary>Deployment blueprint for `Youtube Catalog` Action (click to expand)</summary>

```yaml showLineNumbers
{
  "identifier": "youtubecatalog",
  "title": "YouTubeCatalogAutomation",
  "icon": "Github",
  "schema": {
    "properties": {
      "service_name": {
        "icon": "Github",
        "title": "Service Name",
        "type": "string",
        "description": "All Uppercase"
      }
    },
    "required": [
      "service_name"
    ]
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {}
}

```

<center>
	<img  src='/img/catalog_blueprint.png'  border='1px'  />
</center>

</details>

 
### Create Self-service Actions

Self-service actions in Port allow developers to perform tasks like scaffolding a service or provisioning a cloud resource through an intuitive UI.

#### How It Works

1.  **User Executes Action**: A user triggers an action from Port's UI.

2.  **Payload Sent**: A payload with metadata and inputs is sent to your infrastructure.

3.  **Job Triggered**: A job runs, and the user receives continuous progress updates.

4.  **Update Port**: The action's status, logs, and links are sent back to Port.

#### Step-by-Step Guide to create a Self-service Action for Youtube Playlist Workflow.

1. Navigate to the Self-service page and click the + New Action button.
2. Choose a name and icon for the action.
3. Define the inputs users need to fill out when executing the action.

  
**Action's Frontend:**

<details>
<summary>Self service action frontend (click to expand)</summary>

```json

  {
  "identifier": "create_youtube_catalog",
  "title": "Create YouTube Catalog",
  "icon": "Github",
  "description": "Self Service Action for YouTube Catalog Workflow",
  "trigger": {
    "type": "self-service",
    "operation": "CREATE",
    "userInputs": {
      "properties": {
        "service_name": {
          "icon": "DefaultProperty",
          "title": "Service Name",
          "type": "string"
        }
      },
      "required": [
        "service_name"
      ]
    }
  }
}
```

</details>


**Define Action's Backend**

1. Define an **Invocation Method** of type **GITHUB** to define how the action will be executed.

2. Specify the payload to be sent to your handler.

<details>
<summary> Self service action backend (click to expand)</summary>

```json
{
  "invocationMethod": {
    "type": "GITHUB",
    "org": "your-github-org",
    "repo": "your-github-repo",
    "workflow": "your-workflow-file.yml",
    "workflowInputs": {
      "port_context": {
        "entity": "{{.entity}}",
        "blueprint": "{{.action.blueprint}}",
        "runId": "{{.run.id}}",
        "trigger": "{{ .trigger }}"
      }
    },
    "reportWorkflowStatus": true
  }
}
```

</details>

**Set Guardrails (Optional)**

Manual Approvals: We instruct to set Manual approval while needed. but we will setup to false in this case.  

<details>
<summary>Manual approval congiration (click to expand)</summary>

```json
{
  "requiredApproval": false
}
```
</details>

 
**Execute the Action**

Users can execute the action from the Port UI.

<details>

<summary>Self service action execution (click to expand)</summary>

```json
{
  "status": "SUCCESS",
  "logMessage": "YouTube Data created/Updated",
  "links": [
    {
      "name": "GitHub Workflow",
      "url": "https://github.com/your-github-org/your-github-repo/actions/runs/123456789"
    }
  ]
}
```

</details>

#### Action JSON Structure

<details>

<summary> Here is a basic structure of a self-service action: (click to expand)</summary>

```json


{
  "identifier": "create_youtube_catalog",
  "title": "Create YouTube Catalog",
  "icon": "Github",
  "description": "Automate YouTube Catalog Workflow",
  "trigger": {
    "type": "self-service",
    "operation": "CREATE",
    "userInputs": {
      "properties": {
        "service_name": {
          "icon": "DefaultProperty",
          "title": "Service Name",
          "type": "string"
        }
      },
      "required": [
        "service_name"
      ]
    }
  },
  "invocationMethod": {
    "type": "GITHUB",
    "org": "your-github-org",
    "repo": "your-github-repo",
    "workflow": "your-workflow-file.yml",
    "workflowInputs": {
      "port_context": {
        "entity": "{{.entity}}",
        "blueprint": "{{.action.blueprint}}",
        "runId": "{{.run.id}}",
        "trigger": "{{ .trigger }}"
      }
    },
    "reportWorkflowStatus": true
  },
  "requiredApproval": false
}
```

<center>

  <img  src='/img/portaction.png'  border='1px'  />

</center>

</details>
  
The following GitHub workflow automates fetching data from YouTube and updating Port with the data.


### GitHub Actions Workflow Guide

1. Create `.github/workflows` in your repository.

2. Inside `.github/workflows`, create a YAML file (e.g., `youtube_port_workflow.yml`).

<details>

<summary>Example (click to expand)</summary>

```

<repository-root>/

      └── .github/

          └── workflows/

              └── <workflow-file>.yml

```

</details>

3. Define Workflow in YAML

<details>
<summary>GitHub Workflow (click to expand)</summary>

```yaml showLineNumbers
name: Update YouTube Playlist and Video Entities in Port

on:
  workflow_dispatch:
    inputs:
      port_context:
        required: false
        description:
          Who triggered the action and general context (blueprint, run id, etc...)
        type: string 

jobs:
  update_port_entities:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the code
        uses: actions/checkout@v2

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y jq curl

      - name: Fetch YouTube Playlist and Video Data
        env:
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
        run: |
          PLAYLIST_ID="PL5ErBr2d3QJH0kbwTQ7HSuzvBb4zIWzhy"
          YOUTUBE_API_KEY="${YOUTUBE_API_KEY}"

          # Fetch playlist info
          playlist_response=$(curl -s "https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&id=${PLAYLIST_ID}&key=${YOUTUBE_API_KEY}")
          if echo "$playlist_response" | jq -e '.items | length == 0' > /dev/null; then
            echo "No items found in the playlist info response."
            exit 1
          fi

          item=$(echo "$playlist_response" | jq -r '.items <sup> </sup>')
          playlist_id=$(echo "$item" | jq -r '.id')
          playlist_title=$(echo "$item" | jq -r '.snippet.title')
          playlist_description=$(echo "$item" | jq -r '.snippet.description // "No description available" | select(length > 0) | select(trim | length > 0) or "No description available"')
          published_at=$(echo "$item" | jq -r '.snippet.publishedAt')
          channel_id=$(echo "$item" | jq -r '.snippet.channelId')
          channel_title=$(echo "$item" | jq -r '.snippet.channelTitle')
          thumbnails_default=$(echo "$item" | jq -r '.snippet.thumbnails.default.url // "No thumbnail available"')
          thumbnails_medium=$(echo "$item" | jq -r '.snippet.thumbnails.medium.url // "No thumbnail available"')
          thumbnails_high=$(echo "$item" | jq -r '.snippet.thumbnails.high.url // "No thumbnail available"')
          thumbnails_standard=$(echo "$item" | jq -r '.snippet.thumbnails.standard.url // "No thumbnail available"')
          thumbnails_maxres=$(echo "$item" | jq -r '.snippet.thumbnails.maxres.url // "No thumbnail available"')
          localized_title=$(echo "$item" | jq -r '.snippet.localized.title // "No Localized Title"')
          localized_description=$(echo "$item" | jq -r '.snippet.localized.description // "No Localized Description" | select(length > 0) | select(trim | length > 0) or "No Localized Description"')

          playlist_json=$(echo "{}" | jq \
            --arg identifier "$playlist_id" \
            --arg blueprint "youtube_playlist" \
            --arg title "$playlist_title" \
            --arg link "https://www.youtube.com/playlist?list=$playlist_id" \
            --arg playlistDescription "$playlist_description" \
            --arg publishedAt "$published_at" \
            --arg channelId "$channel_id" \
            --arg channelTitle "$channel_title" \
            --arg default "$thumbnails_default" \
            --arg medium "$thumbnails_medium" \
            --arg high "$thumbnails_high" \
            --arg standard "$thumbnails_standard" \
            --arg maxres "$thumbnails_maxres" \
            --arg localizedTitle "$localized_title" \
            --arg localizedDescription "$localized_description" \
            '
            .identifier = $identifier |
            .blueprint = $blueprint |
            .title = $title |
            .properties.link = $link |
            .properties.playlistDescription = $playlistDescription |
            .properties.publishedAt = $publishedAt |
            .properties.channelId = $channelId |
            .properties.channelTitle = $channelTitle |
            .properties.thumbnails.default = $default |
            .properties.thumbnails.medium = $medium |
            .properties.thumbnails.high = $high |
            .properties.thumbnails.standard = $standard |
            .properties.thumbnails.maxres = $maxres |
            .properties.localized.title = $localizedTitle |
            .properties.localized.description = $localizedDescription
            ')

          combined_json=$(echo "[]" | jq --argjson playlist "$playlist_json" '. + [$playlist]')

          # Fetch playlist items
          next_page_token=""
          while true; do
            playlist_items_response=$(curl -s "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId=${PLAYLIST_ID}&maxResults=50&pageToken=${next_page_token}&key=${YOUTUBE_API_KEY}")
            if echo "$playlist_items_response" | jq -e '.items | length == 0' > /dev/null; then
              echo "No items found in the playlist response."
              break
            fi

            for item in $(echo "$playlist_items_response" | jq -c '.items[]'); do
              video_id=$(echo "$item" | jq -r '.contentDetails.videoId')

              # Fetch video details
              video_response=$(curl -s "https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id=${video_id}&key=${YOUTUBE_API_KEY}")
              if echo "$video_response" | jq -e '.items | length == 0' > /dev/null; then
                echo "No video details found for video ID: $video_id"
                continue
              fi

              video_details=$(echo "$video_response" | jq -r '.items <sup> </sup>')
              duration=$(echo "$video_details" | jq -r '.contentDetails.duration' | awk -F'T' '{print $2}' | sed 's/H/:/g; s/M/:/g; s/S//g' | sed 's/^0*//; s/:0*/:/g; s/^://')
              likes=$(echo "$video_details" | jq -r '.statistics.likeCount // "No likes available"')
              views=$(echo "$video_details" | jq -r '.statistics.viewCount // "No views available"')
              comments=$(echo "$video_details" | jq -r '.statistics.commentCount // "No comments available"')

              title=$(echo "$item" | jq -r '.snippet.title // "No title available"')
              description=$(echo "$item" | jq -r '.snippet.description // "No description available" | select(length > 0) | select(trim | length > 0) or "No description available"')
              published_at=$(echo "$item" | jq -r '.snippet.publishedAt // "No published date available"')
              position=$(echo "$item" | jq -r '.snippet.position // "No position available"')
              thumbnails_default=$(echo "$item" | jq -r '.snippet.thumbnails.default.url // "No thumbnail available"')
              thumbnails_medium=$(echo "$item" | jq -r '.snippet.thumbnails.medium.url // "No thumbnail available"')
              thumbnails_high=$(echo "$item" | jq -r '.snippet.thumbnails.high.url // "No thumbnail available"')
              thumbnails_standard=$(echo "$item" | jq -r '.snippet.thumbnails.standard.url // "No thumbnail available"')
              thumbnails_maxres=$(echo "$item" | jq -r '.snippet.thumbnails.maxres.url // "No thumbnail available"')
              channel_title=$(echo "$item" | jq -r '.snippet.channelTitle // "No channel title available"')
              channel_id=$(echo "$item" | jq -r '.snippet.channelId // "No channel ID available"')

              video_json=$(echo "{}" | jq \
                --arg identifier "$video_id" \
                --arg blueprint "youtube_video" \
                --arg title "$title" \
                --arg link "https://www.youtube.com/watch?v=$video_id" \
                --arg videoDescription "$description" \
                --arg duration "$duration" \
                --arg publishedAt "$published_at" \
                --arg position "$position" \
                --arg likes "$likes" \
                --arg views "$views" \
                --arg comments "$comments" \
                --arg default "$thumbnails_default" \
                --arg medium "$thumbnails_medium" \
                --arg high "$thumbnails_high" \
                --arg standard "$thumbnails_standard" \
                --arg maxres "$thumbnails_maxres" \
                --arg videoOwnerChannelTitle "$channel_title" \
                --arg videoOwnerChannelId "$channel_id" \
                '
                .identifier = $identifier |
                .blueprint = $blueprint |
                .title = $title |
                .properties.link = $link |
                .properties.videoDescription = $videoDescription |
                .properties.duration = $duration |
                .properties.publishedAt = $publishedAt |
                .properties.position = $position |
                .properties.likes = $likes |
                .properties.views = $views |
                .properties.comments = $comments |
                .properties.thumbnails.default = $default |
                .properties.thumbnails.medium = $medium |
                .properties.thumbnails.high = $high |
                .properties.thumbnails.standard = $standard |
                .properties.thumbnails.maxres = $maxres |
                .properties.videoOwnerChannelTitle = $videoOwnerChannelTitle |
                .properties.videoOwnerChannelId = $videoOwnerChannelId |
                .relations.playlist = "$playlist_id"
                ')

              combined_json=$(echo "$combined_json" | jq --argjson video "$video_json" '. + [$video]')
            done

            next_page_token=$(echo "$playlist_items_response" | jq -r '.nextPageToken // ""')
            if [ -z "$next_page_token" ]; then
              break
            fi
          done

          # Save the combined JSON array to the environment variable for Port
          echo "$combined_json" > port_entities.json
          echo "entities=$(jq -c . port_entities.json)" >> $GITHUB_ENV

      - name: Bulk Create/Update YouTube Playlist and Video Entities in Port
        id: bulk_create_update
        uses: port-labs/port-github-action@v1
        with:
          clientId: ${{ secrets.PORT_CLIENT_ID }}
          clientSecret: ${{ secrets.PORT_CLIENT_SECRET }}
          baseUrl: https://api.getport.io
          operation: BULK_UPSERT
          entities: ${{ env.entities }}

      - name: Inform completion of request to Create / Update Catalog in Port
        uses: port-labs/port-github-action@v1
        with:
          clientId: ${{ secrets.PORT_CLIENT_ID }}
          clientSecret: ${{ secrets.PORT_CLIENT_SECRET }}
          baseUrl: https://api.getport.io
          operation: PATCH_RUN
          status: ${{ steps.bulk_create_update.outcome == 'success' && 'SUCCESS' || 'FAILURE' }}
          runId: ${{fromJson(inputs.port_context).runId}}
          logMessage: ${{ steps.bulk_create_update.outcome == 'success' && 'YouTube Data created/Updated Successfully' || 'Error in YouTube Data creation/update' }}
```

</details>


4. Add and push the workflow file to your repository.

5. Go to **Actions** tab in GitHub to see workflow execution.

6. Go to **Settings** > **Secrets** to add Secrets usedin the workflow.

  
<details>

<summary>Here’s an example of what you would see on Port calatog when Playlist and Video data has been injected. (click to expand)</summary>

<center>
<img  src='/img/playlist_catalog.png'  border='1px'  />
</center>
<center>
<img  src='/img/playlist_details.png'  border='1px'  />
</center>
<center>
<img  src='/img/videos_catalog.png'  border='1px'  />
</center>
<center>
<img  src='/img/videos_details.png'  border='1px'  />
</center>
</details>

  
## Step 3: Visualizing Data in Port

By leveraging Port's Dashboards, you can create custom dashboards to do the following :
1. A dashboard for tracking playlist-level metrics like the number of videos.
2. Video-level insights, such as view count, position in playlist, and thumbnail displays.

<details>

<summary> Here’s an example of what you would see (click to expand)</summary>

<center>
<img  src='/img/visualize.png'  border='1px'  />
</center>
 
</details>


### Dashboard setup

1. Go to your [software catalog](https://app.getport.io/organization/catalog).
2. Click on the `+ New` button in the left sidebar.
3. Select **New dashboard**.
4. Name the dashboard ( Visualise Youtube Playlist ), choose an icon if desired, and click `Create`.

### Creating a Dashboard in Port

If you followed through with the dashboard setup, you will have created a new empty dashboard as seen in the last image. Let's get ready to add widgets.

### Adding Widgets

Let's create a widget that displays the number of videos in a YouTube playlist.

<details>
<summary><b>Count of Videos in Playlist (click to expand)</b></summary>

1. Click `+ Widget` and select **Number Chart**.
2. Title: `Number of Videos`. (add the `Metric` icon).
3. Description: `Shows the number of videos on the playlist` (optional).
4. Select `Count entities` for the **Chart type**.
5. Choose **YouTube Video** as the **Blueprint**.
6. Select `count` for the **Function**.  
7. Click `Save`.

    <center>
    <img src="/img/video_counts.png" border="1px" />
    </center>

</details>

#### Creating Other Widgets

You can also create other widgets to display additional data about your YouTube videos such as:

- **Average Number of Likes Across All Videos**

<details>
<summary><b>Average Number of Likes (click to expand)</b></summary>

1. Click `+ Widget` and select **Number Chart**.
2. Title: `Average Likes`. (add the `Metric` icon).
3. Description: `Shows the average number of likes across all videos` (optional).
4. Select `Agregate by property` for the **Chart type**.
5. Choose **YouTube Video** as the **Blueprint**.
6. Select `Like Count` for the **Property**.
6. Select `Average` for the **Function**.
7. Select `total` for the **Average of**.
8. Click `Save`.

    <center>
    <img src="/img/average_likes.png" border="1px" />
    </center>
  

</details>

- **Number of Views a Video Has**

<details>
<summary><b>Number of Views (click to expand)</b></summary>

1. Click `+ Widget` and select **Number Chart**.
2. Title: `Total Views`. (add the `Metric` icon).
3. Description: `Shows the total number of views for all videos` (optional).
4. Select `Agregate by property` for the **Chart type**.
5. Choose **YouTube Video** as the **Blueprint**.
6. Select `View Count` for the **Property**.
7. Select `Sum` for the **Function**.
8. Click `Save`.

    <center>
    <img src="/img/total_views.png" border="1px" />
    </center>
  

</details>

By following these steps, you can effectively automate the process to catalog YouTube playlist and video data into Port.