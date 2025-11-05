# Cloudinary Image Upload Setup Guide

## Overview
This guide shows how to configure Cloudinary for image uploads in the ServiceDesk application. Images are uploaded directly from React to Cloudinary, and only the secure URLs are stored in Django.

## 1. Cloudinary Dashboard Configuration

### Step 1: Create Cloudinary Account
1. Go to [cloudinary.com](https://cloudinary.com)
2. Sign up for a free account
3. Verify your email address

### Step 2: Get Your Credentials
1. Login to your Cloudinary dashboard
2. Go to the **Dashboard** tab
3. Copy these values:
   - **Cloud Name**: `your_cloud_name`
   - **API Key**: `123456789012345`
   - **API Secret**: `abcdefghijklmnopqrstuvwxyz123456`

### Step 3: Create Upload Preset
1. Go to **Settings** → **Upload**
2. Scroll down to **Upload presets**
3. Click **Add upload preset**
4. Configure the preset:
   - **Preset name**: `servicedesk_uploads`
   - **Signing Mode**: `Unsigned` (important!)
   - **Folder**: `servicedesk/tickets` (optional)
   - **Format**: `Auto`
   - **Quality**: `Auto`
   - **Max file size**: `5000000` (5MB)
   - **Allowed formats**: `jpg,png,gif,webp`
5. Click **Save**

## 2. Frontend Configuration

### Update Cloudinary Config
Edit `src/config/cloudinary.js`:

```javascript
export const CLOUDINARY_CONFIG = {
  CLOUD_NAME: 'your_actual_cloud_name',
  UPLOAD_PRESET: 'servicedesk_uploads',
  UPLOAD_URL: 'https://api.cloudinary.com/v1_1/your_actual_cloud_name/image/upload'
}
```

### Update Components
Replace `YOUR_CLOUD_NAME` and `YOUR_UPLOAD_PRESET` in:
- `src/components/forms/TicketForm.jsx`
- `src/components/common/CloudinaryUpload.jsx`

## 3. Backend Configuration

### Environment Variables
Add to your `.env` file:

```bash
# Cloudinary Configuration (optional - only for server-side operations)
CLOUDINARY_CLOUD_NAME=your_actual_cloud_name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123456
```

### Django Settings
Add to `settings.py` (optional):

```python
# Cloudinary settings (for reference only)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}
```

## 4. Database Schema

The ticket table needs an `image_url` column. Since we're using `managed=False`, you need to add this column to your SQLite database manually:

```sql
ALTER TABLE tickets ADD COLUMN image_url TEXT;
```

## 5. Testing the Setup

### Test Upload Flow
1. Start your Django backend: `python manage.py runserver 8002`
2. Start your React frontend: `npm start`
3. Login as any user
4. Click "New Ticket"
5. Fill out the form and select an image
6. Submit the ticket
7. Check that the image appears in the ticket details

### Verify in Cloudinary
1. Go to your Cloudinary dashboard
2. Click **Media Library**
3. You should see your uploaded images in the `servicedesk/tickets` folder

## 6. Security Considerations

### Upload Preset Security
- Use **unsigned** presets for client-side uploads
- Set file size limits (5MB recommended)
- Restrict allowed formats to images only
- Consider adding folder restrictions

### URL Validation
- Always validate that URLs are from your Cloudinary domain
- Consider implementing URL signing for sensitive images

## 7. Troubleshooting

### Common Issues

**Upload fails with 401 Unauthorized**
- Check that your upload preset is set to "Unsigned"
- Verify the preset name matches exactly

**Upload fails with CORS error**
- Cloudinary handles CORS automatically for image uploads
- Ensure you're using the correct upload URL format

**Images don't display**
- Check that the `image_url` field is being saved to the database
- Verify the Cloudinary URLs are accessible
- Check browser console for image loading errors

**File size too large**
- Default limit is 10MB for free accounts
- Adjust the max file size in your upload preset
- Add client-side validation for better UX

### Debug Steps
1. Check browser network tab for failed requests
2. Verify Cloudinary credentials in dashboard
3. Test upload directly using Cloudinary's upload widget
4. Check Django logs for database errors

## 8. Production Considerations

### Performance
- Enable auto-optimization in Cloudinary
- Use responsive image delivery
- Consider implementing lazy loading

### Backup
- Cloudinary provides automatic backups
- Consider periodic exports for critical images

### Monitoring
- Monitor upload success rates
- Set up alerts for failed uploads
- Track storage usage in Cloudinary dashboard

## 9. Example Implementation

### React Upload Component
```javascript
const uploadToCloudinary = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('upload_preset', 'servicedesk_uploads')

  const response = await axios.post(
    'https://api.cloudinary.com/v1_1/your_cloud_name/image/upload',
    formData
  )
  
  return response.data.secure_url
}
```

### Django Model
```python
class Ticket(models.Model):
    # ... other fields ...
    image_url = models.URLField(max_length=500, null=True, blank=True)
```

### Display Component
```javascript
const ImageDisplay = ({ imageUrl }) => (
  imageUrl ? (
    <img 
      src={imageUrl} 
      alt="Ticket attachment" 
      className="w-32 h-32 object-cover rounded-lg"
    />
  ) : null
)
```

This setup provides a complete image upload solution with Cloudinary handling all file storage and Django only storing the secure URLs.