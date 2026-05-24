// Vercel serverless function. Exchanges the static Azure Speech key
// (server-side env var) for a short-lived authorization token the browser
// can use with the Azure Speech SDK. The static key never reaches the
// client.
//
// Required env vars (set in Vercel project settings):
//   SPEECH_KEY    — Key 1 from the Azure Speech resource
//   SPEECH_REGION — the resource's region (e.g. "westeurope")

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");

  const key = process.env.SPEECH_KEY;
  const region = process.env.SPEECH_REGION;

  if (!key || !region) {
    return res.status(503).json({
      error: "speech_not_configured",
      message:
        "Set SPEECH_KEY and SPEECH_REGION in the Vercel project's environment " +
        "variables, then redeploy. See /speech for setup steps.",
    });
  }

  const url = `https://${region}.api.cognitive.microsoft.com/sts/v1.0/issueToken`;

  try {
    const upstream = await fetch(url, {
      method: "POST",
      headers: {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Length": "0",
      },
    });

    if (!upstream.ok) {
      const body = await upstream.text();
      return res.status(502).json({
        error: "azure_token_error",
        status: upstream.status,
        message: body.slice(0, 400),
      });
    }

    const token = await upstream.text();
    return res.status(200).json({ token, region });
  } catch (err) {
    return res.status(500).json({
      error: "fetch_failed",
      message: err && err.message ? err.message : String(err),
    });
  }
}
