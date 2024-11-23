async function postData(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams(data),
  });
  return response.json();
}

document.addEventListener("DOMContentLoaded", function () {
  const generatePrimeABtn = document.querySelector(".generate-prime-a.btn");
  const generatePrimeBBtn = document.querySelector(".generate-prime-b.btn");
  const generateKeyABtn = document.querySelector(".generate-key-a.btn");
  const generateKeyBBtn = document.querySelector(".generate-key-b.btn");
  const encryptMessageBtn = document.querySelector(".encrypt-message.btn");
  const decryptMessageBtn = document.querySelector(".decrypt-message.btn");
  const signatureBtn = document.querySelector(".signature.btn");
  const verifyBtn = document.querySelector(".verify.btn");

  const convertBtn = document.querySelector(".convert.btn");

  if (generatePrimeABtn) {
    generatePrimeABtn.addEventListener("click", async () => {
      const bits = document.getElementById("bits").value;
      if (!bits || bits < 1 || bits > 1024) {
        alert("Bits must be between 1 and 1024.");
        return;
      }
      const data = await postData("/elgamal_signature/genprimea", { bits });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById("p_a").value = BigInt(data.p_a).toString();
      }
    });
  }

  if (generatePrimeBBtn) {
    generatePrimeBBtn.addEventListener("click", async () => {
      const bits = document.getElementById("bits").value;
      if (!bits || bits < 1 || bits > 1024) {
        alert("Bits must be between 1 and 1024.");
        return;
      }
      const data = await postData("/elgamal_signature/genprimeb", { bits });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById("p_b").value = BigInt(data.p_b).toString();
      }
    });
  }

  if (generateKeyABtn) {
    generateKeyABtn.addEventListener("click", async () => {
      const p_a = document.getElementById("p_a").value;
      const alpha_a = document.getElementById("alpha_a").value;
      const a_a = document.getElementById("a_a").value;

      if (!p_a || !alpha_a || !a_a) {
        alert("Please enter values for p_a, alpha_a, and a_a.");
        return;
      }

      const data = await postData("/elgamal_signature/genkeya", {
        p_a,
        alpha_a,
        a_a,
      });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById(
          "beta_a"
        ).innerText = `beta_a = ${data.beta_a.toString()}`;
        document.getElementById(
          "public-key-a"
        ).innerText = `Public Key A: (p_a, alpha_a, beta_a) = (${data.p_a.toString()}, ${data.alpha_a.toString()}, ${data.beta_a.toString()})`;
        document.getElementById(
          "private-key-a"
        ).innerText = `Private Key A: (a_a) = (${data.a_a.toString()})`;
      }
    });
  }

  if (generateKeyBBtn) {
    generateKeyBBtn.addEventListener("click", async () => {
      const p_b = document.getElementById("p_b").value;
      const alpha_b = document.getElementById("alpha_b").value;
      const a_b = document.getElementById("a_b").value;

      if (!p_b || !alpha_b || !a_b) {
        alert("Please enter values for p_b, alpha_b, and a_b.");
        return;
      }

      const data = await postData("/elgamal_signature/genkeyb", {
        p_b,
        alpha_b,
        a_b,
      });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById(
          "beta_b"
        ).innerText = `beta_b = ${data.beta_b.toString()}`;
        document.getElementById(
          "public-key-b"
        ).innerText = `Public Key B: (p_b, alpha_b, beta_b) = (${data.p_b.toString()}, ${data.alpha_b.toString()}, ${data.beta_b.toString()})`;
        document.getElementById(
          "private-key-b"
        ).innerText = `Private Key B: (a_b) = (${data.a_b.toString()})`;
      }
    });
  }

  if (encryptMessageBtn) {
    encryptMessageBtn.addEventListener("click", async () => {
      const k = document.getElementById("k").value;
      const m = document.getElementById("m").value;
      const p_b = document.getElementById("p_b").value;
      const alpha_b = document.getElementById("alpha_b").value;
      const beta_b = document.getElementById("beta_b").innerText.split("= ")[1];

      if (!m || !k || !p_b || !alpha_b || !beta_b) {
        alert("Please enter values for m, k, p_b, alpha_b, and beta_b.");
        return;
      }

      const data = await postData("/elgamal_signature/encrypt", {
        k,
        m,
        p_b,
        alpha_b,
        beta_b,
      });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById("y1-value").innerText = `y1 = ${BigInt(
          data.y1
        ).toString()}`;
        document.getElementById("y2-value").innerText = `y2 = ${BigInt(
          data.y2
        ).toString()}`;
      }
    });
  }

  if (decryptMessageBtn) {
    decryptMessageBtn.addEventListener("click", async () => {
      const y1 = document.getElementById("y1-decrypt").value;
      const y2 = document.getElementById("y2-decrypt").value;
      const p_b = document.getElementById("p_b").value;
      const a_b = document.getElementById("a_b").value;

      if (!y1 || !y2 || !p_b || !a_b) {
        alert("Please enter values for y1, y2, p_b, and a_b.");
        return;
      }
      const data = await postData("/elgamal_signature/decrypt", {
        y1,
        y2,
        p_b,
        a_b,
      });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById(
          "m-decrypt-value"
        ).innerText = `Decrypt: m = ${data.m.toString()}`;
      }
    });
  }

  if (signatureBtn) {
    signatureBtn.addEventListener("click", async () => {
      const m = document.getElementById("m").value;
      const p_a = document.getElementById("p_a").value;
      const alpha_a = document.getElementById("alpha_a").value;
      const a_a = document.getElementById("a_a").value;

      if (!m || !p_a || !alpha_a || !a_a) {
        alert("Please enter values for m, p_a, alpha_a, a_a.");
        return;
      }

      const data = await postData("/elgamal_signature/signature", {
        m,
        p_a,
        alpha_a,
        a_a,
      });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById("gamal-sign").innerText = `γ = ${BigInt(
          data.gamal
        ).toString()}`;
        document.getElementById("sigma-sign").innerText = `σ = ${BigInt(
          data.sigma
        ).toString()}`;
      }
    });
  }

  if (verifyBtn) {
    verifyBtn.addEventListener("click", async () => {
      const m = document.getElementById("m").value;
      const p_a = document.getElementById("p_a").value;
      const alpha_a = document.getElementById("alpha_a").value;
      const beta_a = document.getElementById("beta_a").innerText.split("= ")[1];
      const gamal = document.getElementById("gamal-veri").value;
      const sigma = document.getElementById("sigma-veri").value;

      if (!m || !p_a || !alpha_a || !beta_a || !gamal || !sigma) {
        alert("Please enter values for m, p_a, alpha_a, beta_a, γ, and σ.");
        return;
      }

      const data = await postData("/elgamal_signature/verify", {
        m,
        p_a,
        alpha_a,
        beta_a,
        gamal,
        sigma,
      });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById("veri").innerText = `Verify: ${data.veri}`;
      }
    });
  }

  if (convertBtn) {
    convertBtn.addEventListener("click", async () => {
      const plain = document.getElementById("plain").value;

      if (!plain) {
        alert("Please type your plaintext.");
        return;
      }

      const data = await postData("/elgamal_signature", { plain });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById(
          "plaintext"
        ).innerText = `Plaintext: ${data.plain}`;
      }
    });
  }
});
