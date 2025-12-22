export const analyzeWoundImage = async (imageUri: string): Promise<Blob> => {
  const formData = new FormData();

  formData.append('file', {
    uri: imageUri,
    name: 'wound.jpg',
    type: 'image/jpeg',
  } as any);

  const response = await fetch('http://192.168.1.141:8001/analyze_image', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(err);
  }

  return await response.blob(); // ✅ PDF binaire
};


export const predictSignLanguage = async (imageUri: string) => {
  const formData = new FormData();

  formData.append('file', {
    uri: imageUri,
    name: 'frame.jpg',
    type: 'image/jpeg',
  } as any);

  const response = await fetch('http://192.168.1.141:8002/predict', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(err);
  }

  return await response.json(); // { prediction: "word" }
};
