async function login(req, res) {
  const { email, password } = req.body;

  const user = await User.findOne({
    where: { email },
  });

  const accessToken = generateAccessToken(user);

  res.json({
    accessToken,
  });
}
