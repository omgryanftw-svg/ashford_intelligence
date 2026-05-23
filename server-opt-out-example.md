# Server-Side Example: `ai_opt_out`

This file shows how to read and honor the `ai_opt_out` form field on the server.

If you are currently posting to a third-party form service like Formspree, switch the form `action` to your own endpoint first and then use one of the examples below.

## 1. Node.js / Express

```js
const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.post('/submit-contact', (req, res) => {
  const { firstName, lastName, email, industry, challenge, ai_opt_out } = req.body;

  const optOut = String(ai_opt_out) === '1';

  const submission = {
    firstName,
    lastName,
    email,
    industry,
    challenge,
    aiOptOut: optOut,
    receivedAt: new Date().toISOString(),
  };

  // Example: store submission in your database or CRM
  // saveSubmission(submission);

  // Example: log with opt-out awareness
  console.log('Contact submitted:', {
    email,
    industry,
    aiOptOut: optOut,
  });

  if (optOut) {
    // Avoid retaining user inputs for training or analytics.
    // You may still keep transactional data needed to respond.
  }

  res.redirect('/thank-you');
});

app.listen(3000, () => {
  console.log('Server listening on http://localhost:3000');
});
```

### Notes
- Validate and sanitize all incoming form values.
- If `ai_opt_out` is `1`, avoid sending the raw `challenge` text to training or analytics pipelines.
- Use a separate storage classification for opt-out submissions.

## 2. Python / Flask

```py
from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    industry = request.form.get('industry')
    challenge = request.form.get('challenge')
    ai_opt_out = request.form.get('ai_opt_out', '0') == '1'

    submission = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'industry': industry,
        'challenge': challenge,
        'ai_opt_out': ai_opt_out,
        'received_at': datetime.utcnow().isoformat() + 'Z',
    }

    print('Contact submitted:', {
        'email': email,
        'industry': industry,
        'ai_opt_out': ai_opt_out,
    })

    if ai_opt_out:
        # Respect the user's choice by not sending data into model training
        # or other improvement pipelines.
        pass

    # save_submission(submission)

    return redirect('/thank-you')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

### Notes
- Use `request.form.get('ai_opt_out', '0') == '1'` to preserve a strict boolean value.
- If the opt-out box is checked, treat the submission as a privacy-sensitive request.
- Keep the form action consistent with your server endpoint.

## 3. HTML form action example

```html
<form action="/submit-contact" method="POST">
  <!-- existing contact fields -->
  <input type="hidden" name="ai_opt_out" value="0" id="aiOptOutHidden">
</form>
```

If you want to keep using Formspree or another hosted form service, you can still include the hidden field there and configure their webhook or integration to preserve it.
