
async function postData(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(data),
    });
    return response.json();
}
document.addEventListener("DOMContentLoaded", function () {
    const generatePrimeBtn = document.querySelector(".generate-prime.btn");
    const submitBtn = document.querySelector(".rsa-submit.btn");
    const generatePrimeEEBtn = document.querySelector(".generate-prime-e.btn");
    const encryptBtn = document.querySelector(".encrypt.btn");
    const decryptBtn = document.querySelector(".decrypt.btn");
    const generateKeysBtn = document.querySelector(".generate-keys.btn");
    const convertBtn = document.querySelector(".convert.btn");
    if (generatePrimeBtn) {
      generatePrimeBtn.addEventListener("click", async () => {
        const bits = document.getElementById("bits").value;
        if (!bits || bits < 1 || bits > 2049) {
          alert("Bits must be between 1 and  2048.");
          return;
        }

        const data = await postData("/rsa/genprime", { bits });
        if (data.error) {
          alert(data.error);
        } else {
          // Automatically fill in p and q values
          document.getElementById("p").value = BigInt(data.p).toString();
          document.getElementById("q").value = BigInt(data.q).toString();
        }
      });
    }
    if (submitBtn) {
      submitBtn.addEventListener("click", async () => {
        const p = document.getElementById("p").value;
        const q = document.getElementById("q").value;

        if (!p || !q) {
          alert("Please enter values for p, q");
          return;
        }
        const data = await postData("/rsa/submit", { p, q });
        if (data.error) {
          alert(data.error);
        } else {
          document.getElementById(
            "n-value"
          ).innerText = `Result: n = ${data.n}`;
          document.getElementById(
            "phi-value"
          ).innerText = `Result: φ(n) = ${data.phi_n}`;
        }
      });
    }

    if (generatePrimeEEBtn) {
      generatePrimeEEBtn.addEventListener("click", async () => {
        const bitse = document.getElementById("bitse").value;

        if (!bitse || bitse < 1 || bitse > 4097) {
          alert("Bits must be between 1 and 4096.");
          return;
        }

        const data = await postData("/rsa/genprimeee", { bitse });
        if (data.error) {
          alert(data.error);
        } else {
          // Automatically fill in p and q values
          document.getElementById("e").value = BigInt(data.e).toString();
        }
      });
    }

    if (generateKeysBtn) {
      generateKeysBtn.addEventListener("click", async () => {
        const p = document.getElementById("p").value;
        const q = document.getElementById("q").value;
        const e = document.getElementById("e").value;

        if (!p || !q || !e) {
          alert("Please enter values for p, q, and e.");
          return;
        }

        const data = await postData("/rsa/genprivatekey", { p, q, e });
        if (data.error) {
          alert(data.error);
        } else {
          document.getElementById("d-value").innerText = `Result: d = ${BigInt(
            data.d
          ).toString()}`;
          document.getElementById(
            "public-key"
          ).innerText = `Public Key: (n, e) = (${data.n}, ${e})`;
          document.getElementById(
            "private-key"
          ).innerText = `Private Key: (n, d) = (${data.n}, ${data.d})`;
        }
      });
    }

    if (encryptBtn) {
      encryptBtn.addEventListener("click", async () => {
        const m = document.getElementById("m").value;
        const e = document.getElementById("e").value;
        const n = document.getElementById("n-value").innerText.split("= ")[1];

        if (!m || !e || !n) {
          alert("Please enter values for m, e, and ensure n is calculated.");
          return;
        }

        const data = await postData("/rsa/encrypt", { m, e, n });
        if (data.error) {
          alert(data.error);
        } else {
          document.getElementById(
            "c-value"
          ).innerText = `Encrypted: c = ${BigInt(data.c).toString()}`;
        }
      });
    }

    if (decryptBtn) {
      decryptBtn.addEventListener("click", async () => {
        const c = document.getElementById("c-decrypt").value;
        const d = document.getElementById("d-value").innerText.split("= ")[1];
        const n = document.getElementById("n-value").innerText.split("= ")[1];

        if (!c || !d || !n) {
          alert("Please enter values for c and ensure d and n are calculated.");
          return;
        }

        const data = await postData("/rsa/decrypt", { c, d, n });
        if (data.error) {
          alert(data.error);
        } else {
          document.getElementById(
            "m-decrypt-value"
          ).innerText = `Decrypted: m = ${BigInt(data.m).toString()}`;
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

        const data = await postData("/rsa", { plain });
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
