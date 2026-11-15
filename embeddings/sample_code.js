async function login(req, res) {
  const { email, password } = req.body;

  const user = await User.findOne({
    where: { email },
  });

  const valid = await bcrypt.compare(password, user.password);

  if (!valid) {
    return res.status(401).json({
      message: "Invalid credentials",
    });
  }

  const accessToken = generateAccessToken(user);

  res.json({
    accessToken,
  });
}

async function register(req, res) {
  const { email, password } = req.body;

  const existingUser = await User.findOne({
    where: { email },
  });

  if (existingUser) {
    return res.status(409).json({
      message: "User already exists",
    });
  }

  const hashedPassword = await bcrypt.hash(password, 10);

  const user = await User.create({
    email,
    password: hashedPassword,
  });

  res.status(201).json({
    message: "User registered successfully",
    user,
  });
}

async function logout(req, res) {
  res.clearCookie("refreshToken");

  res.json({
    message: "Logged out successfully",
  });
}
