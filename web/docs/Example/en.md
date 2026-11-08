# R2 Cloud Upload

Uploads images to Cloudflare R2 bucket and returns the public URL.

## Description

This node takes an image input and uploads it to a Cloudflare R2 bucket. It requires R2 credentials (bucket name, account ID, access key ID, and secret access key) which should be configured in the node's settings panel.

## Inputs

### Required

| Parameter         | Type   | Description                                                            |
|-------------------|--------|------------------------------------------------------------------------|
| `image`           | IMAGE  | The image to upload to R2                                              |
| `bucket_name`     | STRING | The name of the R2 bucket                                              |
| `account_id`      | STRING | Cloudflare account ID                                                  |
| `access_key_id`   | STRING | R2 access key ID                                                       |
| `secret_access_key`| STRING | R2 secret access key                                                   |
| `public_url_base` | STRING | The public URL base for accessing the file (e.g., https://pub-xxx.r2.dev) |

### Optional

| Parameter   | Type   | Description                                              |
|-------------|--------|----------------------------------------------------------|
| `file_name` | STRING | Custom filename (auto-generated if empty)                |

## Outputs

| Output | Type   | Description                    |
|--------|--------|--------------------------------|
| `url`  | STRING | The public URL of the uploaded file |

## Setup Instructions

1. Create a Cloudflare R2 bucket in your Cloudflare dashboard
2. Create an R2 API token with read/write permissions
3. Note your Account ID from the R2 overview page
4. Configure the node with your credentials
5. Optionally set a custom public URL base if using a custom domain

## Notes

- If `file_name` is not provided, the node will auto-generate a unique filename with timestamp
- Images are always uploaded in PNG format
- The node returns the public URL that can be used to access the uploaded file
