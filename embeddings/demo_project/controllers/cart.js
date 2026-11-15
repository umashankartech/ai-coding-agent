async function addToCart(req, res) {
  const { productId, quantity } = req.body;

  await Cart.create({
    productId,
    quantity,
  });

  res.json({
    message: "Product added to cart",
  });
}
