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
  const submitBtn = document.querySelector(".rsa-sig-submit.btn");
  const submitBBtn = document.querySelector(".rsa-sig-submit-b.btn");
  const generatePrimeEEBtn = document.querySelector(".generate-prime-e.btn");
  const generatePrimeBBtn = document.querySelector(".generate-prime-b.btn");
  const generatePrimeEBBtn = document.querySelector(".generate-prime-b-e.btn");

  const encryptBtn = document.querySelector(".encrypt-mes.btn");
  const decryptBtn = document.querySelector(".decrypt.btn");
  const generateKeysBtn = document.querySelector(".generate-keys.btn");
  const generateKeysBBtn = document.querySelector(".generate-keys-b.btn");
  const convertBtn = document.querySelector(".convert.btn");
  const encryptSigBtn = document.querySelector(".encrypt-sig.btn");
  const decryptSigBtn = document.querySelector(".decrypt-sig.btn");

  if (generatePrimeBtn) {
    generatePrimeBtn.addEventListener("click", async () => {
      const bits = document.getElementById("bits").value;

      if (!bits || bits < 1 || bits > 2049) {
        alert("Bits must be between 1 and 2048.");
        return;
      }

      const data = await postData("/rsa_signature/genprime", { bits });
      if (data.error) {
        alert(data.error);
      } else {
        // Automatically fill in p and q values
        document.getElementById("p_a").value = BigInt(data.p_a).toString();
        document.getElementById("q_a").value = BigInt(data.q_a).toString();
      }
    });
  }

  if (submitBtn) {
    submitBtn.addEventListener("click", async () => {
      const p_a = document.getElementById("p_a").value;
      const q_a = document.getElementById("q_a").value;

      if (!p_a || !q_a) {
        alert("Please enter values for p, q");
        return;
      }
      n_a = BigInt(p_a) * BigInt(q_a); // Sử dụng BigInt để xử lý số lớn
      phi_n_a = (BigInt(p_a) - 1n) * (BigInt(q_a) - 1n); // Cần "1n" để tương thích với BigInt
      document.getElementById(
        "n_a"
      ).innerText = `Result: n = ${n_a.toString()}`; // Hiển thị số không bị làm tròn
      document.getElementById(
        "phi_n_a"
      ).innerText = `Result: φ(n) = ${phi_n_a.toString()}`;
    });
  }

  if (submitBBtn) {
    submitBBtn.addEventListener("click", async () => {
      const p_b = document.getElementById("p_b").value;
      const q_b = document.getElementById("q_b").value;

      if (!p_b || !q_b) {
        alert("Please enter values for p, q");
        return;
      }
      n_b = BigInt(p_b) * BigInt(q_b); // Sử dụng BigInt để xử lý số lớn
      phi_n_b = (BigInt(p_b) - 1n) * (BigInt(q_b) - 1n); // Cần "1n" để tương thích với BigInt
      document.getElementById(
        "n_b"
      ).innerText = `Result: n = ${n_b.toString()}`; // Hiển thị số không bị làm tròn
      document.getElementById(
        "phi_n_b"
      ).innerText = `Result: φ(n) = ${phi_n_b.toString()}`;
    });
  }

  if (generatePrimeEEBtn) {
    generatePrimeEEBtn.addEventListener("click", async () => {
      const bitse = document.getElementById("bitse").value;

      if (!bitse || bitse < 1 || bitse > 4097) {
        alert("Bits must be between 1 and 4096.");
        return;
      }

      const data = await postData("/rsa_signature/genprimeee", { bitse });
      if (data.error) {
        alert(data.error);
      } else {
        // Automatically fill in p and q values
        document.getElementById("e_a").value = BigInt(data.e_a).toString();
      }
    });
  }

  if (generateKeysBtn) {
    generateKeysBtn.addEventListener("click", async () => {
      const p_a = document.getElementById("p_a").value;
      const q_a = document.getElementById("q_a").value;
      const e_a = document.getElementById("e_a").value;

      if (!p_a || !q_a || !e_a) {
        alert("Please enter values for p, q, and e.");
        return;
      }

      const data = await postData("/rsa_signature/genprivatekey", {
        p_a,
        q_a,
        e_a,
      });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById("d_a").innerText = `Result: d_a = ${BigInt(
          data.d_a
        ).toString()}`;
        document.getElementById(
          "public-key"
        ).innerText = `Public Key: (n, e) = (${data.n_a}, ${e_a})`;
        document.getElementById(
          "private-key"
        ).innerText = `Private Key: (n, d) = (${data.n_a}, ${data.d_a})`;
      }
    });
  }

  if (generateKeysBBtn) {
    generateKeysBBtn.addEventListener("click", async () => {
      const p_b = document.getElementById("p_b").value;
      const q_b = document.getElementById("q_b").value;
      const e_b = document.getElementById("e_b").value;

      if (!p_b || !q_b || !e_b) {
        alert("Please enter values for p, q, and e.");
        return;
      }

      const data = await postData("/rsa_signature/genprivatekeyb", {
        p_b,
        q_b,
        e_b,
      });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById("d_b").innerText = `Result: d_b = ${BigInt(
          data.d_b
        ).toString()}`;
        document.getElementById(
          "public-key-b"
        ).innerText = `Public Key B: (n, e) = (${data.n_b}, ${e_b})`;
        document.getElementById(
          "private-key-b"
        ).innerText = `Private Key: (n, d) = (${data.n_b}, ${data.d_b})`;
      }
    });
  }

  if (generatePrimeBBtn) {
    generatePrimeBBtn.addEventListener("click", async () => {
      const bitsb = document.getElementById("bitsb").value;

      if (!bitsb || bitsb < 1 || bitsb > 2049) {
        alert("Bits must be between 1 and 2048.");
        return;
      }

      const data = await postData("/rsa_signature/genprimeb", { bitsb });
      if (data.error) {
        alert(data.error);
      } else {
        // Automatically fill in p and q values
        document.getElementById("p_b").value = BigInt(data.p_b).toString();
        document.getElementById("q_b").value = BigInt(data.q_b).toString();
      }
    });
  }

  if (generatePrimeEBBtn) {
    generatePrimeEBBtn.addEventListener("click", async () => {
      const bitsbe = document.getElementById("bitsbe").value;

      if (!bitsbe || bitsbe < 1 || bitsbe > 4097) {
        alert("Bits must be between 1 and 4096.");
        return;
      }

      const data = await postData("/rsa_signature/genprimeeeb", { bitsbe });
      if (data.error) {
        alert(data.error);
      } else {
        // Automatically fill in p and q values
        document.getElementById("e_b").value = BigInt(data.e_b).toString();
      }
    });
  }

  if (encryptBtn) {
    encryptBtn.addEventListener("click", async () => {
      const m = document.getElementById("m").value;
      const e_b = document.getElementById("e_b").value;
      const n_b = document.getElementById("n_b").innerText.split("= ")[1];

      if (!m || !e_b || !n_b) {
        alert("Please enter values for m, e, and ensure n is calculated.");
        return;
      }

      const data = await postData("/rsa_signature/encrypt", { m, e_b, n_b });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById("c-value").innerText = `Encrypted: c = ${BigInt(
          data.c
        ).toString()}`;
      }
    });
  }

  if (decryptBtn) {
    decryptBtn.addEventListener("click", async () => {
      const c = document.getElementById("c-decrypt").value;
      const d_b = document.getElementById("d_b").innerText.split("= ")[1];
      const n_b = document.getElementById("n_b").innerText.split("= ")[1];

      if (!c || !d_b || !n_b) {
        alert("Please enter values for c and ensure d and n are calculated.");
        return;
      }

      const data = await postData("/rsa_signature/decrypt", { c, d_b, n_b });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById(
          "m-decrypt-value"
        ).innerText = `Decrypted: m = ${BigInt(data.m).toString()}`;
      }
    });
  }

  if (encryptSigBtn) {
    encryptSigBtn.addEventListener("click", async () => {
      const m = document.getElementById("m").value;
      const n_a = document.getElementById("n_a").innerText.split("= ")[1];
      const d_a = document.getElementById("d_a").innerText.split("= ")[1];

      if (!m || !d_a || !n_a) {
        alert("Please enter values for m and ensure d and n are calculated.");
        return;
      }

      const data = await postData("/rsa_signature/signature", { m, d_a, n_a });
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById("sig").innerText = `Signature: sig = ${BigInt(
          data.sig
        ).toString()}`;
      }
    });
  }

  if (decryptSigBtn) {
    decryptSigBtn.addEventListener("click", async () => {
      const m = document.getElementById("m").value;
      const n_a = document.getElementById("n_a").innerText.split("= ")[1];
      const e_a = document.getElementById("e_a").value;
      const sig = document.getElementById("sig-veri").value;
      if (!m || !e_a || !n_a || !sig) {
        alert("Please enter values for m and ensure d and n are calculated.");
        return;
      }

      const data = await postData("/rsa_signature/verify", {
        m,
        e_a,
        n_a,
        sig,
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

      const data = await postData("/rsa_signature", { plain });
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
